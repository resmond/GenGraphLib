from collections import namedtuple
from typing import Self, NamedTuple

import datetime as dt
from enum import IntEnum, StrEnum

LineRefList: type = list[ int ]

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

KeyValueTuple: type = tuple[str, str]
KeyRecordList: type = list[KeyValueTuple]
KeyRecordPacket: type = tuple[int, KeyRecordList ]
KeyValuePacket: type = tuple[int, str]
ModelPropTypes: type = type[ str, int, float, dt.datetime, StrEnum, IntEnum, bool]

class IndexInfo:

    def __init__(
            self: Self,
            keyinfo_id:  str,
            key:         str,
            alias:       str,
            index_type:  KeyIndexType,
            index_state: KeyIndexState,
            hitpct:      float,
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

        self.hitpct:  float   = hitpct
        self.keycnt:  int   = keycnt
        self.refcnt:  int   = refcnt
        self.unique:  bool  = unique

IndexPacket: type = namedtuple(
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

IndexMsgTuple: type = tuple[str, str, str, KeyIndexType, KeyIndexState, float, int, int, bool ]

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
    def from_packet( cls, keyindex_packet: IndexPacket ):
        message = cls( *keyindex_packet )
        return message

class SerializationType( IntEnum ):
    Pickle          = 1
    Parquet         = 2
    EqualKeyValLine = 3
    ColonKeyValLine = 4
    CSV             = 5
