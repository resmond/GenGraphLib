from abc import abstractmethod
from collections import namedtuple
from typing import Self, Protocol, NamedTuple
import pyarrow as par

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
ModelPropTypes: type = type[ str, int, float, dt.datetime, StrEnum, IntEnum, bool]

class ImportValueInterface[ T: ModelPropTypes ]( Protocol ):

    def recv_import( self: Self, row_num: int, import_value: T ) -> None: ...
    def finalize( self: Self, maxrecnum: int ) -> None: ...
    def get_pararray( self: Self ) -> par.Array | None:  ...

class KeyType( IntEnum ):
    KStr    = 1        #utf8
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
        super().__init__()
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
            keyinfo_id:  str,
            key:         str,
            alias:       str,
            index_type:  KeyIndexType,
            index_state: KeyIndexState,
            hitpct:      int,
            keycnt:      int,
            refcnt:      int,
            unique:      bool
        ) -> None:
        super().__init__()

        self.keyinfo_id:  str           = keyinfo_id
        self.key:         str           = key
        self.alias:       str           = alias
        self.index_type:  KeyIndexType  = index_type
        self.index_state: KeyIndexState = index_state

        self.hitpct:  int   = hitpct
        self.keycnt:  int   = keycnt
        self.refcnt:  int   = refcnt
        self.unique:  bool  = unique

KeyIndexPacket: type = namedtuple(
        "KeyIndexPacket",
        [
                    "keyinfo_id",
                    "key",
                    "alias",
                    "index_type",
                    "index_state",
                    "hitpct",
                    "keycnt",
                    "refcnt",
                    "isunique"
                   ])

keyIndexMsgTuple: type = tuple[str, KeyIndexType, KeyIndexState, int, int, bool ]

class KeyIndexMsg(NamedTuple):
    keyinfo_id:    str
    key:           str
    alias:         str
    index_type:    KeyIndexType
    index_state:   KeyIndexState
    hitpct:        int
    keycnt:        int
    refcnt:        int
    isunique:      bool

    def to_packet( self: Self ) -> tuple:
        return ( 
            self.keyinfo_id,
            self.key,
            self.alias,
            self.index_type,
            self.index_state,
            self.hitpct,
            self.keycnt,
            self.refcnt,
            self.isunique
        )

    @classmethod
    def from_packet( cls, keyindex_packet: KeyIndexPacket ):
        message = cls( *keyindex_packet )
        return message

class SerializationType( IntEnum ):
    Pickle          = 1
    Parquet         = 2
    EqualKeyValLine = 3
    ColonKeyValLine = 4
    CSV             = 5

class KeyDefInterface( Protocol ):
    key:      str
    alias:    str
    keytype:  KeyType
    pytype:   type
    partype:  par.DataType
    groupids: list[str]

KeyDefDict:  type = dict[ str, KeyDefInterface ]

class KeyDefRoot( Protocol ):

    def graph_id(self: Self) -> str:
        pass

    def __getitem__(self, key: str) -> KeyDefInterface:
        pass

class ColumnInterface( Protocol ):
    id: str
    key_def: KeyDefInterface
    keytype: KeyType
    partype:  par.DataType
    index_dir: str

class DefaultMapOfLists[ T ]( dict[ str, list[T] ] ):

    def add_entry( self: Self, key: str, value: T ) -> None:
        if key not in self:
            self[key] = list[T]()
        self[key].append( value )

class KeyInfo:

    def __init__(
            self: Self,
            keytype:  KeyType,
            pytype:   type,
            partype:  par.DataType,
            key:      str,
            alias:    str,
            groupids: list[str]
        ):
        super().__init__()
        self.keytype:   KeyType          = keytype
        self.pytype:    type             = pytype
        self.partype:   par.DataType = partype

        self.key:       str       = key
        self.alias:     str       = alias
        self.groupids:  list[str] = groupids

    @property
    def graph_id( self: Self ) -> str:
        return f"{self.batch_id}@{self.key}"

class KeyValSchemaInfo:

    def __init__( self: Self, keys: list[KeyInfo], groups: list[str], active_groups: list[str] | None = None, active_keys: list[str] | None = None ):
        super().__init__()
        self.keys:          list[KeyInfo]    = keys
        self.groups:        list[str]        = groups
        self.active_groups: list[str] | None = active_groups
        self.active_keys:   list[str] | None = active_keys

# class BootLogInfo:
#
#     def __init__(
#             self: Self,
#             boot_id: str,
#             boot_index: int,
#             first_dt: dt.datetime,
#             last_dt: dt.datetime,
#             dir_name: str,
#             dir_path: str,
#             keys_path: str | None = None
#         ) -> None:
#         super().__init__()
#         self.boot_id: str                = boot_id
#         self.boot_index:    int          = boot_index
#         self.first_dt:      dt.datetime  = first_dt
#         self.last_dt:       dt.datetime  = last_dt
#         self.dir_name:      str          = dir_name
#         self.dir_path:      str          = dir_path
#         self.keys_path: str | None       = keys_path
