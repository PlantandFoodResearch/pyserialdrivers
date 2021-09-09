from pyserialdrivers.exo.constants import Param


def test_code_has_unit(param: Param):
    param1 = Param(param.name)
    param2 = Param(param.code)
    assert param == param1 == param2
