# Change scope
# noinspection PyUnresolvedReferences
from pyserialdrivers.exo._gen_constants import _ParamCodes, _ParamUnits, _ParamNames


class Param(object):
    _code_to_name = dict([(v, k) for (k, v) in _ParamCodes.items()])

    def __init__(self, name_or_code):
        if isinstance(name_or_code, str):
            name = name_or_code
            code = _ParamCodes.get(name_or_code)
        elif isinstance(name_or_code, int):
            code = name_or_code
            name = Param._code_to_name.get(code)
        else:
            raise ValueError(f"Unknown parameter: {name_or_code}")
        description = _ParamNames.get(name)
        unit = _ParamUnits.get(name)
        if not all([description, code, unit]):
            raise ValueError(f"Unknown parameter: {name}")
        self._name = name
        self._code = int(code)
        self._unit = unit
        self._description = description

    def __eq__(self, other):
        if isinstance(other, Param):
            return other.name == self.name
        elif isinstance(other, str):
            return other == self.name
        elif isinstance(other, int):
            return other == self.code
        return False

    def __repr__(self):
        return f"Parameter: {self._name}"

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def unit(self):
        return self._unit

    @property
    def description(self):
        return self._description


class Commands:
    class Get:
        SERIAL = b"sn"  # Get sonde serial number
        TIME = b"time"
        PARA = b"para"
        DATA = b"data"
        WIPE = b"hwipesleft"

    class Set:
        TIME = b"time {hh}:{mm}:{ss}"
        WIPE = b"twipeb"

    EOL = b"\r"
    DELIM = b" "
