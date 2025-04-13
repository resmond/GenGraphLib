from collections.abc import Callable
import datetime as dt
from enum import IntEnum
from typing import Self

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

class SerializationType( IntEnum ):
    CSV = 1
    JArray = 2
    JObject = 3

class DictOfLists[T]( dict[ str, list[T] ] ):

    def __init__( self: Self ) -> None:
        super().__init__()

    def add_entry( self: Self, key: str, value: T ) -> None:
        if key not in self:
            self[key] = []
        self[key].append( value )
