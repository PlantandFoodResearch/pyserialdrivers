from pyserialdrivers.exo.DCPBase import DCPBase
from io import RawIOBase
from telnetlib import Telnet
from typing import Optional


class _TelnetToRawIO(RawIOBase):
    def __init__(self, telnet: Telnet):
        self._telnet = telnet
        self._buffer = bytes()
        super(_TelnetToRawIO, self).__init__()

    def read(self, size: int = ...) -> Optional[bytes]:
        while True:
            self._buffer += self._telnet.read_very_eager()
            if size == -1:
                ret_val = self._buffer
                self._buffer = bytes()
                break
            elif len(self._buffer) >= size:
                ret_val = self._buffer[:size]
                self._buffer = self._buffer[size:]
                break
            # read some telnet data
            # self._buffer += self._telnet.read_until(b"#", timeout=1)
        return ret_val

    def write(self, __b) -> Optional[int]:
        self._telnet.write(__b)
        return len(__b)


class DCPTelnet(DCPBase):
    def __init__(self, host: str, port=23):
        self._telnet = Telnet(host, port)
        self.interface = _TelnetToRawIO(self._telnet)
        super(DCPTelnet, self).__init__()
