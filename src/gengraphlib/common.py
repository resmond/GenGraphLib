from typing import Self, Protocol

import datetime as dt

from collections.abc import Iterable
from dataclasses import dataclass
from enum import IntEnum, StrEnum

LineRefList: type = list[ int ]
KeyFilter:   type = dict[ str, str | None ]

KeyGroupRec  = tuple[str] | tuple[str, str] | tuple[ str, str, Iterable[str] ]
keygroup_rec = tuple[str, str, str | None, list[str] | None]

IValueTuple: type = tuple[int, str]
SValueTuple: type = tuple[str, str]

KeyValTypes: type = type[ str, int, bool, float, dt.datetime ]
#process_fields_fn = Callable[ [ dict[ str, KeyValTypes ], int, str], bool ]
KValueDict: type  = dict[ str, KeyValTypes ]

KeyValueTuple: type = tuple[str, str]
KeyRecordList: type = list[KeyValueTuple]
KeyRecordPacket: type = tuple[int, KeyRecordList ]
KeyValuePacket: type = tuple[int, str]

class KeyType( IntEnum ):
    KStr    = 1
    KInt    = 2
    KBool   = 3
    KFloat  = 4
    KTmst   = 5

class KeyIndexType(StrEnum):
    Undetermined      = "Undetermined"
    IntIdent          = "IntIdent"
    IntSorted         = "IntSorted"
    StrTokens         = "StrTokens"
    StrSorted         = "StrSorted"
    StrParsed         = "StrParsed"
    StrLogged         = "StrLogged"
    FloatSorted       = "FloatSorted"
    BoolDualIntersect = "BoolDualIntersect"
    TmstSorted        = "TmstSorted"

@dataclass
class KeyIndexState(IntEnum):
    Uninitialized = 0
    Initialized   = 1
    Running       = 2
    Finished      = 3
    Error         = 4

@dataclass
class keyIndexInfo:
    keyinfo_id: str
    index_type: KeyIndexType = KeyIndexType.Undetermined
    state: KeyIndexState = KeyIndexState.Uninitialized
    valuecnt: int = 0
    instancecnt: int = 0
    unique: bool = False

class SerializationType( IntEnum ):
    CSV             = 1
    JArray          = 2
    JObject         = 3
    Pickle          = 4
    Jline           = 5
    EqualKeyValLine = 6
    ColonKeyValLine = 7

class KeyDefInterface( Protocol ):
    key:      str
    alias:    str
    keytype:  KeyType
    groupids: list[str] | None

KeyDefDict:  type = dict[ str, KeyDefInterface ]

KeyValueEvent: type = tuple[int, int, memoryview]
#value_event_fn = Callable[ [ KeyValueEvent ], None ]

class KeyValuesInterface( Protocol ):
    id: str
    key_def: KeyDefInterface
    keytype: KeyType
    index_dir: str
    def value_event( self: Self, keyvalue_event: KeyValueEvent ) -> None: ...

class DefaultMapOfLists[ T ]( dict[ str, list[T] ] ):

    def add_entry( self: Self, key: str, value: T ) -> None:
        if key not in self:
            self[key] = list[T]()
        self[key].append( value )
