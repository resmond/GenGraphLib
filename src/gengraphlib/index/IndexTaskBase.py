from abc import abstractmethod
from typing import Self

import multiprocessing as mp

from ..common import (
    KeyValTypes,
    KeyType,
    KeyIndexType,
    keyIndexInfo,
    KeyIndexState,
    KeyInfo,
    IndexTaskInterface,
    BootLogInfo
)

from ..columns import GraphTable

class IndexTaskBase[ T: KeyValTypes ]( IndexTaskInterface ):

    def __init__( self: Self, key_info: KeyInfo, bootlog_info: BootLogInfo, graph_table: GraphTable, app_msgqueue: mp.Queue, end_event: mp.Event  ) -> None:
        super().__init__()
        self._isproc:    bool    = False
        self.status_cnt: int     = 100

        self.key_info:     KeyInfo      = key_info
        self.bootlog_info: BootLogInfo  = bootlog_info
        self.graph_table:  GraphTable   = graph_table
        self.app_msgqueue: mp.Queue     = app_msgqueue
        self.end_event:    mp.Event     = end_event

        self.boot_id:    str = self.bootlog_info.schema_bootid
        self.keyinfo_id: str = f"{self.boot_id}@{key_info.key}"

        self.key:        str     = key_info.key
        self.alias:      str     = key_info.alias
        self.keytype :   KeyType = key_info.keytype

        self.index_type:  KeyIndexType  = KeyIndexType.Undetermined
        self.index_state: KeyIndexState = KeyIndexState.Uninitialized

        self.refmax:   float   = 1
        self.keycnt:   float   = 0
        self.refcnt:   float   = 0
        self.isunique: bool    = True

    def is_proc( self: Self ) -> bool:
        return self._isproc

    def id( self: Self ) -> str:
        return f'index-{self.key}'

    def get_index_info( self: Self ) -> keyIndexInfo:
        return keyIndexInfo(
            keyinfo_id=self.keyinfo_id,
            key=self.key,
            alias=self.alias,
            index_type=self.index_type,
            index_state=self.index_state,
            hitpct = round( self.refcnt / self.refmax * 100 ),
            keycnt= int( self.keycnt ),
            refcnt= int( self.refcnt ),
            unique=self.isunique
        )

    @abstractmethod
    def main_loop( self: Self, queue: mp.Queue, end_event: mp.Event ) -> None:
        pass

    @abstractmethod
    def apply_tocolumn( self: Self, maxrecnum: int ) -> bool:
        pass

    #def dump_sortedstr( self: Self, strdict: SortedDict[str, LineRefList ] ):




