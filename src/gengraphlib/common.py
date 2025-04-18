from collections.abc import Callable, Iterable
import datetime as dt
from enum import IntEnum
from typing import Self, Protocol

LineRefList: type = list[ int ]
KeyFilter:   type = dict[ str, str | None ]

KeyGroupRec  = tuple[str] | tuple[str, str] | tuple[ str, str, Iterable[str] ]
keygroup_rec = tuple[str, str, str | None, list[str] | None]

IValueTuple: type = tuple[int, str]
SValueTuple: type = tuple[str, str]

KeyValTypes: type = type[ str, int, bool, float, dt.datetime ]
process_fields_fn = Callable[ [ dict[ str, KeyValTypes ], int, str], bool ]
KValueDict: type  = dict[ str, KeyValTypes ]

class KeyType( IntEnum ):
    KStr    = 1
    KInt    = 2
    KBool   = 3
    KFloat  = 4
    KTmst   = 5

class SerializationType( IntEnum ):
    CSV     = 1
    JArray  = 2
    JObject = 3

class KeyDefInterface( Protocol ):
    key:      str
    alias:    str
    keytype:  KeyType
    groupids: list[str] | None

KeyDefDict:  type = dict[ str, KeyDefInterface ]

KeyValueEvent: type = tuple[int, int, memoryview]
value_event_fn = Callable[ [ KeyValueEvent ], None ]
class KeyValuesInterface( Protocol ):
    keytype: KeyType
    value_event_fn: value_event_fn
    def value_event( self: Self, keyvalue_event: KeyValueEvent ) -> None: ...

class DictOfLists[T]( dict[ str, list[T] ] ):

    def __init__( self: Self ) -> None:
        super().__init__()

    def add_entry( self: Self, key: str, value: T ) -> None:
        if key not in self:
            self[key] = []
        self[key].append( value )
