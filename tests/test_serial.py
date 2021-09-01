import datetime
from unittest.mock import patch

import pytest
from serial import SerialBase
from pyserialdrivers.exo.constants import Commands, ParamCodes
from pyserialdrivers.exo.serial import DCPSerial, _DEFAULT_TIMEOUT


def test_dcp2_basic():
    with patch("pyserialdrivers.exo.serial.Serial", spec=SerialBase) as mock_serial:
        exo = DCPSerial("COM12")
        mock_serial.assert_called_once_with(
            port="COM12", baudrate=9600, timeout=_DEFAULT_TIMEOUT
        )
        assert exo.interface == mock_serial.return_value
        mock_serial.reset_mock()
        exo = DCPSerial("COM12", baudrate=115200)
        mock_serial.assert_called_once_with(
            port="COM12", baudrate=115200, timeout=_DEFAULT_TIMEOUT
        )
        assert exo.interface == mock_serial.return_value


def test_dcp2_parameter_detection(patch_serial, make_exo):
    exo = make_exo(ParamCodes)
    # Lazy initialisation
    _ = exo.params
    for param in ParamCodes:
        assert param in exo.params


def test_dcp2_data(patch_serial, make_exo):
    exo = make_exo([ParamCodes.TEMP_C, ParamCodes.TURB_N])
    _ = exo.params
    patch_serial.responses.update({b"data" + Commands.EOL: b"20 2" + Commands.EOL})
    exo.update()
    dp = exo.get(ParamCodes.TEMP_C)
    assert dp.value == 20.0
    assert dp.param == ParamCodes.TEMP_C
    dp = exo.get(ParamCodes.TURB_N)
    assert dp.value == 2.0
    assert dp.param == ParamCodes.TURB_N
    patch_serial.responses.update({b"data" + Commands.EOL: b"21 3" + Commands.EOL})
    exo.update()
    dp = exo.get(ParamCodes.TEMP_C)
    assert dp.value == 21.0
    dp = exo.get(ParamCodes.TURB_N)
    assert dp.value == 3.0


def test_dcp2_datetime(patch_serial, make_exo):
    exo = make_exo([ParamCodes.YYMMDD, ParamCodes.HHMMSS])
    _ = exo.params
    dt = datetime.datetime.now()
    dt_yymmdd = dt.strftime("%y%m%d").encode()
    dt_hhmmss = dt.strftime("%H%M%S").encode()
    patch_serial.responses.update(
        {b"data" + Commands.EOL: dt_yymmdd + b" " + dt_hhmmss + Commands.EOL}
    )
    exo.update()
    dp = exo.get(ParamCodes.YYMMDD)
    assert dp.value == dt.date()
    dp = exo.get(ParamCodes.HHMMSS)
    low_res_dt = dt.time()
    low_res_dt = low_res_dt.replace(microsecond=0, tzinfo=None)
    assert dp.value == low_res_dt


def test_dcp2_bad_data(patch_serial, make_exo):
    exo = make_exo([ParamCodes.TEMP_C, ParamCodes.BATT_V])
    _ = exo.params
    with pytest.raises(ValueError) as exc:
        patch_serial.responses.update({b"data" + Commands.EOL: b"20.0" + Commands.EOL})
        exo.update()
    with pytest.raises(ValueError) as exc:
        patch_serial.responses.update({b"data" + Commands.EOL: b"1 2 3" + Commands.EOL})
        exo.update()


def test_dcp2_values(patch_serial, make_exo):
    params = [ParamCodes.TEMP_C, ParamCodes.BATT_V, ParamCodes.TURB_N]
    exo = make_exo(params)
    _ = exo.params
    patch_serial.responses.update({b"data" + Commands.EOL: b"2.5 3.7 5" + Commands.EOL})
    values = exo.values
    # test dict repr
    values_d = exo.values_dict()
    for value, param in zip(values, params):
        assert value.param == param
        assert param.name in values_d
