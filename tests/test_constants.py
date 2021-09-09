from pyserialdrivers.exo.constants import ParamCodes, ParamUnits


def test_code_has_unit(paramcode: ParamCodes):
    pcode2 = ParamCodes(paramcode.value)
    pcode3 = ParamCodes[paramcode.name]
    # pcode1 = getattr(ParamCodes, paramcode.name)
    assert paramcode == pcode2 == pcode3
    assert ParamUnits[paramcode.name]
    assert isinstance(paramcode.unit, str)
    assert isinstance(paramcode.description, str)
