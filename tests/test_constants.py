from pyserialdrivers.exo.constants import ParamCodes, ParamUnits


def test_code_has_unit(paramcode: ParamCodes):
    assert ParamUnits[paramcode.name]
    assert isinstance(paramcode.unit, str)
    assert isinstance(paramcode.description, str)
