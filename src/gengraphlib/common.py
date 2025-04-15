from collections.abc import Callable, Iterable
import datetime as dt
from enum import IntEnum
from typing import Self, Protocol


KeyValTypes: type = type[str, int, bool, dt.datetime, float]
process_fields_fn = Callable[ [ dict[ str, KeyValTypes ], int, str], bool ]
keygroup_rec = tuple[str, str, str | None, list[str] | None]
KeyFilter: type = dict[str, str | None ]
KeyGroupRec = tuple[str] |tuple[str, str] | tuple[str, str, Iterable[str]]

IValueTuple: type = tuple[int, str]
SValueTuple: type = tuple[str, str]

class KeyType( IntEnum ):
    KStr         = 1
    KInt         = 2
    KBool        = 3
    KTimeStamp   = 4
    KFloat       = 5

class KeyDefInterface[ T: KeyValTypes ]( Protocol ):
    json_key: str
    log_key: str
    key_type: KeyType
    groups: list[str] | None

KeyDefDict:  type = dict[ str, KeyDefInterface ]
LineRefList: type = list[ int ]

KValueDict: type = dict[str, KeyValTypes]

KeyValueEvent: type = tuple[int, int, memoryview]

value_event_fn = Callable[ [ KeyValueEvent ], None ]

class KeyValuesInterface( Protocol ):
    key_type: KeyType
    value_event_fn: value_event_fn

    def value_event( self: Self, keyvalue_event: KeyValueEvent ) -> None: ...

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
