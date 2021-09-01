import pytest
from pyserialdrivers.exo.telnet import DCPTelnet


@pytest.mark.timeout(5)
def test_connect(telnet_host):
    exo = DCPTelnet(telnet_host)
    params = exo.params
    assert params
    values = exo.values
    assert values
    print(values)
