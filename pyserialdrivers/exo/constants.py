from enum import Enum

# Change scope
# noinspection PyUnresolvedReferences
from pyserialdrivers.exo._gen_constants import ParamCodes, ParamUnits, ParamNames


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
