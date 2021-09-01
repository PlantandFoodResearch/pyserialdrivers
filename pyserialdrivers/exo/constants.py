from enum import Enum

# Change scope
# noinspection PyUnresolvedReferences
from pyserialdrivers.exo._gen_constants import ParamCodes, ParamUnits, ParamNames


class Commands:
    class Get(Enum):
        SERIAL = "ssn"  # Get sonde and sensor serial numbers
        TIME = "time"
        PARAM = "para"
        DATA = "data"

    class Set(Enum):
        TIME = "time {hh}:{mm}:{ss}"

    EOL = b"\r"
    DELIM = b" "
