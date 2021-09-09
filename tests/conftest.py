from typing import List
import logging
import os
import dummyserial
import pytest
from serial import SerialBase
import socketserver
from socket import timeout
import threading
from unittest.mock import patch

logging.basicConfig(level=logging.DEBUG)


def pytest_generate_tests(metafunc):
    if "param" in metafunc.fixturenames:
        from pyserialdrivers.exo.constants import _ParamCodes, Param

        metafunc.parametrize("param", [Param(x) for x in _ParamCodes.values()])


@pytest.fixture()
def patch_serial() -> dummyserial.Serial:
    # Silence dummyserial
    from pyserialdrivers.exo.serial import _DEFAULT_BAUDRATE

    dummy = dummyserial.Serial(port="COM50", baudrate=_DEFAULT_BAUDRATE)
    dummy._logger.setLevel(logging.INFO)
    with patch("pyserialdrivers.exo.serial.Serial", spec=SerialBase) as mock:
        # All possible parameters
        mock.return_value = dummy
        yield dummy


@pytest.fixture()
def make_exo(patch_serial):
    from pyserialdrivers.exo.constants import Param, Commands
    from pyserialdrivers.exo.serial import DCPSerial

    def _make_exo(params: List["Param"]):
        patch_serial.responses.update(
            {
                Commands.Get.SERIAL + Commands.EOL: b"abc123",
                Commands.Get.WIPE + Commands.EOL: b"0",
            }
        )
        resp = b" ".join([str(x.code).encode() for x in params]) + Commands.EOL
        patch_serial.responses.update({Commands.Get.PARA + Commands.EOL: resp})
        # All possible parameters
        exo = DCPSerial("COM12")
        return exo

    return _make_exo


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    responses = {}

    def handle(self):
        self.request.settimeout(1)
        while not self.server._BaseServer__is_shut_down.is_set():
            try:
                data = str(self.request.recv(1024), "ascii")
            except (TimeoutError, timeout):
                continue
            except ConnectionAbortedError:
                break
            if data in ThreadedTCPRequestHandler.responses.keys():
                response = ThreadedTCPRequestHandler.responses[data]
            else:
                cur_thread = threading.current_thread()
                response = bytes("{}: {}\r".format(cur_thread.name, data), "ascii")
            self.request.sendall(response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


@pytest.fixture(scope="session")
def find_free_port():
    """
    Returns a factory that finds the next free port that is available on the OS
    This is a bit of a hack, it does this by creating a new socket, and calling
    bind with the 0 port. The operating system will assign a brand new port,
    which we can find out using getsockname(). Once we have the new port
    information we close the socket thereby returning it to the free pool.
    This means it is technically possible for this function to return the same
    port twice (for example if run in very quick succession), however operating
    systems return a random port number in the default range (1024 - 65535),
    and it is highly unlikely for two processes to get the same port number.
    In other words, it is possible to flake, but incredibly unlikely.
    """

    def _find_free_port():
        import socket

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", 0))
        portnum = s.getsockname()[1]
        s.close()

        return portnum

    return _find_free_port


@pytest.fixture(scope="function")
def telnet_server(find_free_port):
    ip = "0.0.0.0"
    port = find_free_port()
    server = ThreadedTCPServer((ip, port), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    try:
        yield server
    finally:
        server.shutdown()
        server.server_close()


@pytest.fixture(scope="session")
def telnet_host() -> str:
    host = os.environ.get("HOST_TELNET")
    if not host:
        pytest.skip("Skipping tests that need a real device. Set env HOST_TELNET")
    # Todo, maybe prep the device or connection
    yield host
