from abc import abstractmethod
from collections import namedtuple
from typing import Self, Protocol, NamedTuple

import datetime as dt
import multiprocessing as mp

from collections.abc import Iterable
from enum import IntEnum, StrEnum

LineRefList: type = list[ int ]
KeyFilter:   type = dict[ str, str | None ]

KeyGroupRec  = tuple[str] | tuple[str, str] | tuple[ str, str, Iterable[str] ]
keygroup_rec = tuple[str, str, str | None, list[str] | None]

IValueTuple: type = tuple[int, str]
SValueTuple: type = tuple[str, str]

VectorValTypes: type = type[ None, str, int, bool, float, dt.datetime ]

KeyValTypes: type = type[ str, int, bool, float, dt.datetime ]
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

class KeyIndexState(IntEnum):
    Uninitialized = 0
    Initialized   = 1
    Running       = 2
    Finished      = 3
    Error         = 4

class TaskType( IntEnum ):
    Undefined = 0
    Main = 1
    StreamSource = 2
    StreamSink = 3
    KeyValProcessor = 4

class TaskState( IntEnum ):
    Init = 1
    Running = 2
    Stopped = 3

class Startable(Protocol):
    @abstractmethod
    def id( self ) -> str: ...
    @abstractmethod
    def is_proc( self ) -> bool: ...
    def start( self: Self ) -> None: ...
    def stop( self: Self ) -> None: ...
    @abstractmethod
    def main_loop( self: Self, *args, **kargs ) -> None: ...

class IndexTaskInterface(Startable):

    def __init( self: Self ) -> None:
        self.key: str            = ""
        self.alias: str          = ""
        self.index_dir: str      = ""
        self.index_filepath: str = ""

    @property
    @abstractmethod
    def queue( self: Self ) -> mp.Queue: ...

class ProcType(IntEnum):
    Undefined = 0
    Main = 1
    StreamSource = 2
    StreamSink = 3
    KeyValProcessor = 4

class ProcState(IntEnum):
    Init = 1
    Running = 2
    Stopped = 3

class ProcRegistry(Protocol):
    def register_proc( self, proc: Startable ) -> None: ...


class keyIndexInfo:

    def __init__(
            self: Self,
            keyinfo_id: str,
            key: str,
            alias: str,
            index_type: KeyIndexType,
            valuecnt: int = 0,
            instancecnt: int = 0,
            unique: bool = False
        ) -> None:
        super().__init__()

        self.keyinfo_id: str          = keyinfo_id
        self.key: str                 = key
        self.alias: str               = alias
        self.index_type: KeyIndexType = index_type
        self.value_cnt: int           = valuecnt
        self.instance_cnt: int        = instancecnt
        self.is_unique: bool          = unique

#"KeyIndexPacket",
# [ "keyinfo_id",  -  str
#   "index_type",  -  KeyIndexType
#   "index_state", -  KeyIndexState
#   "value_cnt",   -  int
#   "instance_cnt",-  int
#   "is_unique"    -  bool
# ]
KeyIndexPacket: type = namedtuple(
        "KeyIndexPacket",
        [
                    "keyinfo_id",
                    "index_type",
                    "index_state",
                    "value_cnt",
                    "instance_cnt",
                    "is_unique"
                   ])

keyIndexMsgTuple: type = tuple[str, KeyIndexType, KeyIndexState, int, int, bool ]

class KeyIndexMsg(NamedTuple):
    keyinfo_id:    str
    index_type:    KeyIndexType
    index_state:   KeyIndexState
    value_cnt:     int
    instance_cnt:  int
    is_unique:     bool

    def to_packet( self: Self ) -> tuple:
        return ( 
            self.keyinfo_id,
            self.index_type,
            self.index_state,
            self.value_cnt,
            self.instance_cnt,
            self.is_unique
        )

    @classmethod
    def from_packet( cls, keyindex_packet: KeyIndexPacket ):
        message = cls( *keyindex_packet )
        return message

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

#KeyValueEvent: type = tuple[int, int, memoryview]

class KeyValuesInterface( Protocol ):
    id: str
    key_def: KeyDefInterface
    keytype: KeyType
    index_dir: str

class DefaultMapOfLists[ T ]( dict[ str, list[T] ] ):

    def add_entry( self: Self, key: str, value: T ) -> None:
        if key not in self:
            self[key] = list[T]()
        self[key].append( value )

class KeyInfo:

    def __init__( self: Self, schema_id: str, key: str, alias: str, keytype: KeyType, groupids: list[str] | str | None = None ):
        self.schema_id: str       = schema_id
        self.key:       str       = key
        self.alias:     str       = alias
        self.keytype:   KeyType   = keytype
        self.groupids:  list[str] | str | None = groupids

    @property
    def keyinfo_id( self: Self ) -> str:
        return f"{self.schema_id}@{self.key}"

class KeyValSchemaInfo:

    def __init__( self: Self, keys: list[KeyInfo], groups: list[str], active_groups: list[str] | None = None, active_keys: list[str] | None = None ):
        self.keys:          list[KeyInfo]    = keys
        self.groups:        list[str]        = groups
        self.active_groups: list[str] | None = active_groups
        self.active_keys:   list[str] | None = active_keys

class BootLogInfo:

    def __init__(
            self: Self,
            schema_bootid: str,
            boot_index: int,
            first_dt: dt.datetime,
            last_dt: dt.datetime,
            dir_name: str,
            dir_path: str,
            keys_path: str | None = None
        ) -> None:
        self.schema_bootid: str          = schema_bootid
        self.boot_index:    int          = boot_index
        self.first_dt:      dt.datetime  = first_dt
        self.last_dt:       dt.datetime  = last_dt
        self.dir_name:      str          = dir_name
        self.dir_path:      str          = dir_path
        self.keys_path: str | None       = keys_path
