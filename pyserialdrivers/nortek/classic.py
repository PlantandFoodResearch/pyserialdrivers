from typing import Union
from pyserialdrivers import MICROPYTHON
from pyserialdrivers.nortek.constants import Commands
from pyserialdrivers.nortek.base import NortekBase

if MICROPYTHON:
    from machine import UART
else:
    from serial import Serial

_DEFAULT_TIMEOUT = 1
_DEFAULT_BAUDRATE = 9600


class Classic(NortekBase):
    def __init__(self, serial_port: Union[str, int], baudrate: int = _DEFAULT_BAUDRATE, timeout: float = _DEFAULT_BAUDRATE):
        """
        Creates object and initialises contact with the device using given serial settings.
        Args:
            serial_port: Either a string or an integer for MICROPYTHON devices.
            baudrate: E.g. 9600
            timeout: Float in seconds
        """
        super().__init__()
        if MICROPYTHON:
            self.interface = UART(serial_port)
            self.interface.init(baudrate=_DEFAULT_BAUDRATE, timeout_chars=_DEFAULT_TIMEOUT)
        else:
            self.interface = Serial(serial_port, baudrate=_DEFAULT_BAUDRATE, timeout=_DEFAULT_TIMEOUT)

        resp = self._command(Commands.Get.SERIAL)
