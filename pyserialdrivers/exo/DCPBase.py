import logging
import time
import typing
from abc import ABC
from datetime import datetime
from io import RawIOBase
from typing import Any, List, Optional, AnyStr, Union

from pyserialdrivers.exo.constants import Commands, ParamCodes

log = logging.getLogger(__name__)

try:
    import threading
except ImportError as e:
    log.exception("Failed to import threading, maybe not supported", e)
    threading = None


class DataPoint:
    def __init__(self, param: ParamCodes, value: Any):
        self._param = param
        self._value = value

    @property
    def param(self) -> ParamCodes:
        return self._param

    @property
    def value(self) -> Any:
        return self._value

    def __index__(self):
        """Enforces unique access in lists"""
        return self.param.value

    def __repr__(self):
        return f"{self.param.description}: {self.value} {self.param.unit}"


class DCPBase(ABC):
    """DCP Interface"""

    interface: "RawIOBase" = (
        None  # The method for interacting with the sensor, e.g. Serial
    )
    _WIPE_TIMEOUT_S = 120
    _WIPE_PERIOD_S = 60 * 60 * 12

    def __init__(self):
        self._params: List[ParamCodes] = []
        self._buffer = bytes()
        self._latest_values: typing.Dict[DataPoint] = dict()
        self._initialised = False
        self._serial: Optional[str] = None
        self._shutdown: Optional[threading.Event] = (
            threading.Event() if threading else None
        )
        self._thread: Optional[threading.Thread] = None

    @property
    def params(self) -> List[ParamCodes]:
        if not self._params:
            # Lazy param initialisation
            self._init_parameters()
        return self._params

    def _init_parameters(self):
        resp = self._command(Commands.Get.PARA)
        if not resp:
            raise ValueError("Could not get parameter list from device")
        param_codes = map(int, DCPBase._split_resp(resp))
        for code in param_codes:
            try:
                param = ParamCodes(code)
                if param in self._params:
                    raise ValueError(
                        "Invalid parameter initialisation, cannot have same"
                        " parameter twice"
                    )
                self._params.append(param)
            except BaseException as e:
                log.error(f"Unknown parameter code: {code}")
                raise e

    @staticmethod
    def _split_resp(resp: AnyStr) -> List[AnyStr]:
        if isinstance(resp, str):
            return resp.split(Commands.DELIM.decode())
        elif isinstance(resp, bytes):
            return resp.split(Commands.DELIM)

    def _init_command_communications(self):
        # spam a few CR to wake up device
        for _ in range(2):
            self.interface.write(Commands.EOL)
            time.sleep(0.1)
        # Echo mode maybe hopefully off. Check for serial number response
        self.interface.write(Commands.Get.SERIAL + Commands.EOL)
        time.sleep(0.5)
        # Raw read all pending data
        buff = self.interface.read(self.interface.inWaiting())
        if not buff:
            raise IOError("Failed to initialise command channel with EXO")
        buff = buff.decode().rstrip().strip()
        self._serial = buff
        self._initialised = True

    def _send(self, data):
        """Send command or raw data to the sensor via the interface"""
        if not self._initialised:
            self._init_command_communications()
        elif isinstance(data, str):
            data = data.encode()
        data = bytes(data)
        if not data.endswith(Commands.EOL):
            data = data + Commands.EOL
        self.interface.write(data)
        # When echo mode is off, we can't gurantee CRs will be rceived.
        # Guess we just have to busy wait :(
        time.sleep(0.5)

    def _read(self, blocking=False) -> Optional[AnyStr]:
        """Read a single response. If blocking, then wait for Commands.EOL"""
        while True:
            self._buffer += self.interface.read(self.interface.inWaiting())
            if blocking and not Commands.EOL in self._buffer:
                time.sleep(0.1)
                continue
            if self._buffer:
                resp = self._buffer.decode().strip().rstrip()
                self._buffer = bytes()
                return resp
            return None

    def update(self):
        """Updates all values via a poll sequence to the sensor"""
        if self.is_wiping:
            log.warning("Attempted to get data whilst sensor is being wiped, skipping")
            return
        resp = self._command(Commands.Get.DATA)
        values = DCPBase._split_resp(resp)
        # The order will match params order
        if not values:
            raise ValueError("Failed to update sensor values, empty response")
        if len(values) != len(self.params):
            raise ValueError("Failed to update sensor values, incorrect data readings")
        for param in self.params:
            # Assume all non datetime are floats, could be unsafe
            value = values.pop(0)
            try:
                if param is ParamCodes.DDMMYY:
                    value = datetime.strptime(value, "%d%m%y").date()
                elif param is ParamCodes.MMDDYY:
                    value = datetime.strptime(value, "%m%d%y").date()
                elif param is ParamCodes.YYMMDD:
                    value = datetime.strptime(value, "%y%m%d").date()
                elif param is ParamCodes.HHMMSS:
                    value = datetime.strptime(value, "%H%M%S").time()
                else:
                    value = float(value)
            finally:
                dp = DataPoint(param, value)
            self._latest_values[dp.param.name] = dp

    def _command(self, command: Union[Commands.Get, Commands.Set]):
        """
        Perform the basic request/response logic of an EXO command.

        E.g. send "data\n" and process the response
        """
        self._send(command)
        # handle weird wipe command response. sometimes triggers another empty response. Trigger double read!
        if command is Commands.Get.WIPE:
            resp = self._read()
            if resp:
                return resp
            self._send(command)
            time.sleep(0.5)
        return self._read()

    def get(self, param: ParamCodes) -> typing.Optional[DataPoint]:
        if param.name in self._latest_values:
            return self._latest_values[param.name]

    def values_dict(self) -> typing.Dict:
        """Return a disctionary of all the current readings"""
        resp = {}
        for value in self._latest_values.values():
            resp.update(
                {
                    value.param.name: {
                        "value": value.value,
                        "unit": value.param.unit,
                        "description": value.param.description,
                    }
                }
            )
        return resp

    @property
    def values(self) -> typing.List[DataPoint]:
        """Get and return latest readings from sensor"""
        self.update()
        if not self._latest_values:
            raise ValueError("No values present")
        return [dp for dp in self._latest_values.values()]

    @property
    def is_wiping(self) -> bool:
        resp = self._command(Commands.Get.WIPE)
        if resp and int(resp) == 0:
            return False
        return True

    def wipe(self, blocking: bool = True):
        """Perform a sensor wipe and optionally attempt to block"""
        resp = self._command(Commands.Set.WIPE)
        # Whilst the documentation states this should return estimated seconds to wipe,
        # experimentally we see an empty response.
        if not blocking:
            return
        begin = time.time()
        if resp:
            wipe_time_remaining = float(resp)
            log.info(f"Wipe initiated, blocking for {wipe_time_remaining}s")
            if wipe_time_remaining > 60:
                raise TimeoutError(f"Expected wipetime too long! {wipe_time_remaining}")
            time.sleep(wipe_time_remaining)
        while self.is_wiping:
            time.sleep(1.0)
            if (time.time() - begin) > self._WIPE_TIMEOUT_S:
                raise TimeoutError("Wiping took too long")

    def _periodic_wipe(self, period):
        """Wipe and requeue self"""
        if not self._shutdown:
            raise ValueError("Bad threaded state")
        log.debug("Periodic wiper thread starting")
        while not self._shutdown.is_set():
            begin = time.time()
            self.wipe()
            elapsed = time.time() - begin
            if elapsed > period:
                elapsed = period
            try:
                self._shutdown.wait(period - elapsed)
            except TimeoutError:
                continue
        log.debug("Periodic wiper thread shutting down")

    def set_start_periodic_wiping(self, period: float = None):
        """Start periodic wiping event (using threads)."""
        if not threading:
            log.error(
                "Cannot start wiping, threading is not supported on this platform"
            )
            return
        if not period:
            period = self._WIPE_PERIOD_S
        self._thread = threading.Thread(target=self._periodic_wipe, args=(period,))
        log.info(f"Starting asynchronous wiping on thread {self._thread}")
        self._thread.start()

    def stop_wiping(self):
        if self._shutdown and self._thread:
            self._shutdown.set()
            self._thread.join()
            self._shutdown = threading.Event()
            self._thread = None

    def __del__(self):
        self.stop_wiping()
