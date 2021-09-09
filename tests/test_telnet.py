import pytest
from pyserialdrivers.exo.constants import Commands, ParamCodes
from pyserialdrivers.exo.telnet import DCPTelnet


def test_telnet_basic(telnet_server):
    ip, port = telnet_server.server_address
    resp = " ".join(
        [str(ParamCodes["TEMP_C"].value), str(ParamCodes["TURB_N"].value)]
    ).encode()
    resp += b"\r"
    telnet_server.RequestHandlerClass.responses = {
        "sn\r": b"abc123\r",
        "para\r": resp,
    }
    # try:
    exo = DCPTelnet(host="127.0.0.1", port=port)
    _ = exo.params
    # except ConnectionAbortedError as exc:
    #     if (
    #         "An established connection was aborted by the software in your host machine"
    #         in exc.strerror
    #     ):
    #         pytest.skip("Could not establish connection, probably firewall / antivirus")
    #     else:
    #         raise exc
