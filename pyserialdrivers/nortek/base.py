import struct
from io import RawIOBase
from typing import Union, Optional

from pyserialdrivers.nortek.constants import Commands

class NortekBase:
    """Base class for Nortek instruments.

    Mostly as per N3015-023-Integrators-Guide-Classic_0821.pdf
    """

    def __init__(self):
        self._buffer = bytes()
        self._latest_values = dict()
        self._initialised = False
        self.interface: Optional["RawIOBase"] = None

    def command(self, command: Union[Commands.Get, Commands.Set]) -> str:
        pass

    def _init_command_communications(self):
        # Todo: implement
        self._initialised = True

    def _send(self, data):
        """Send command or raw data to the sensor via the interface

        Args:
            data: Either bytes or str, already in the Little Endian format
        """
        if not self._initialised:
            self._init_command_communications()
        elif isinstance(data, str):
            data = data.encode()
        data = bytes(data)
        self.interface.write(data)


    def

    def _command(self, command: bytes) -> bytes:
        """
        Validates and converts command to little endian bytes, sends it, and awaits response (until timeout)
        Args:
            command:

        Returns:
            bytes: The response, converted to big endian
        """
        if len(command) != 2:
            raise ValueError("Nortek Classic commands must be 2 ASCII bytes long")
        raw = int.from_bytes(command, "big").to_bytes(2, "little")  # Revert order, since we know length
        self._send(raw)
