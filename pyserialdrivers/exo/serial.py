from serial import Serial

from pyserialdrivers.exo.DCPBase import DCPBase

_DEFAULT_TIMEOUT = 1
_DEFAULT_BAUDRATE = 9600


class DCPSerial(DCPBase):
    def __init__(self, serial_port, baudrate=_DEFAULT_BAUDRATE):
        """Set interface first, then call baseclass initializer"""
        self.interface = Serial(
            port=serial_port, baudrate=baudrate, timeout=_DEFAULT_TIMEOUT
        )
        super(DCPSerial, self).__init__()
