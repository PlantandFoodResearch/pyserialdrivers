# Change scope
# noinspection PyUnresolvedReferences
from pyserialdrivers.exo._gen_constants import _ParamCodes, _ParamUnits, _ParamNames, _Params


class Param(object):
    def __init__(self, name):
        param = _Params.get(name)
        if not param:
            ValueError(f"Unknown parameter: {name}")
        code, unit, description = param
        self._name = name
        self._code = int(code)
        self._unit = unit
        self._description = description

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


class MinimalEnum(object):
    def __new__(cls, *args, **kwargs):
        base_dict = "_" + cls.__name__
        obj = super(MinimalEnum, cls).__new__(cls)
        # Cache link to base and inverse lookup dictionaries
        if not hasattr(cls, "_base"):
            setattr(cls, "_base", globals().get(base_dict))
        if not hasattr(cls, "_inverse_lookup"):
            setattr(cls, "_inverse_lookup", dict([(v, k) for (k, v) in cls._base.items()]))
        # for name in cls._base:
        #     value = cls._base[name]
        #     setattr(cls, name, value)
        return obj

    def __init__(self, value):
        super().__init__()
        if value not in self._inverse_lookup:
            raise ValueError(f"Invalid enum instantiations: {self.__name} does not contain value {value}")
        self._value = value
        self._name = self._inverse_lookup.get(value)

    def __class_getitem__(cls, name):
        if name in cls._base.keys():
            return cls(cls._base.get(name))
        raise TypeError("Invalid enum")

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._name == other._name
        if isinstance(other, str):
            return self._name == other
        return False

    @classmethod
    def __next__(cls):
        pass

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> str:
        return self._value


class ParamCodes(MinimalEnum):
    @property
    def unit(self) -> str:
        return ParamUnits[self.name].value

    @property
    def description(self) -> str:
        return ParamNames[self.name].value


class ParamUnits(MinimalEnum):
    pass


class ParamNames(MinimalEnum):
    pass


obj = ParamCodes(1)
del obj
obj = ParamUnits("NTU")
del obj
obj = ParamNames("Temperature")
del obj


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
