import sys


from pyserialdrivers.exo.DCPBase import DCPBase

_DEFAULT_TIMEOUT = 1
_DEFAULT_BAUDRATE = 9600


MICROPYTHON = False
# Protect for micropython version
if "micropython" in str(sys.implementation):
    MICROPYTHON = True

if not MICROPYTHON:
    from serial import Serial
else:
    from machine import UART

    class SerialCompat(UART):
        def inWaiting(self):
            return self.any()


class DCPSerial(DCPBase):
    def __init__(self, serial_port, baudrate=_DEFAULT_BAUDRATE):
        """Set interface first, then call baseclass initializer"""
        if MICROPYTHON:
            self.interface = SerialCompat(int(serial_port))
            self.interface.init(baudrate=baudrate, timeout_chars=_DEFAULT_TIMEOUT)
        else:
            self.interface = Serial(
                port=serial_port, baudrate=baudrate, timeout=_DEFAULT_TIMEOUT
            )
        super(DCPSerial, self).__init__()
