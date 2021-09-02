import time
from unittest import mock

import pytest

from pyserialdrivers.exo._gen_constants import ParamCodes
from pyserialdrivers.exo.constants import Commands


def test_wiping_blocking(patch_serial, make_exo):
    params = [
        ParamCodes.TEMP_C,
        ParamCodes.BATT_V,
        ParamCodes.TURB_N,
        ParamCodes.WIPE_V,
    ]
    exo = make_exo(params)
    _ = exo.params
    patch_serial.responses.update(
        {
            b"twipeb" + Commands.EOL: b"0.1" + Commands.EOL,
            b"hwipesleft" + Commands.EOL: b"0" + Commands.EOL,
        }
    )
    exo.wipe()


@pytest.mark.timeout(10)
def test_periodic_wiping(patch_serial, make_exo):
    _period = 0.5
    _grace_period = 1.0
    params = [
        ParamCodes.TEMP_C,
        ParamCodes.BATT_V,
        ParamCodes.TURB_N,
        ParamCodes.WIPE_V,
    ]
    exo = make_exo(params)
    with mock.patch.object(exo, "wipe", autospec=True) as mock_wipe:
        exo.set_start_periodic_wiping(_period)
        thread = exo._thread
        begin = time.time()
        while mock_wipe.call_count < 3:
            time.sleep(0.1)
        exo.stop_wiping()
        end = time.time()
        assert end - begin >= (2 * _period) < (2 * _period + _grace_period)
        time.sleep(1.0)
        assert mock_wipe.call_count == 3
    assert not thread.is_alive()
    assert not exo._thread
