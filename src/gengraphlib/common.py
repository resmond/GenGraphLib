from collections.abc import Callable
import datetime as dt
from enum import IntEnum

KeyValTypes: type = type[str, int, bool, dt.datetime, float]
process_fields_fn = Callable[ [ dict[ str, KeyValTypes ], int, str], bool ]
keygroup_rec = tuple[str, str, str | None, list[str] | None]
KeyFilter: type = dict[str, str | None ]

class KeyType( IntEnum ):
    KStr         = 1
    KInt         = 2
    KBool        = 3
    KTimeStamp   = 4
    KFloat       = 5
