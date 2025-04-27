from abc import abstractmethod
from typing import Self

import os.path
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

from ..columns.Column import Column

class IndexTaskBase[ T: KeyValTypes ]( IndexTaskInterface ):

    def __init__( self: Self, key_info: KeyInfo, bootlog_info: BootLogInfo, app_msgqueue: mp.Queue, end_event: mp.Event ) -> None:
        super(IndexTaskBase,self).__init__( f"{key_info.key}-index" )

        self.status_cnt: int     = 100
        self.key:        str     = key_info.key
        self.alias:      str     = key_info.alias
        self.key_info:   KeyInfo = key_info
        self.keytype:    KeyType = key_info.keytype
        self._isproc:    bool    = False

        self._app_msgqueue:    mp.Queue       = app_msgqueue
        self._end_event:       mp.Event       = end_event

        self._bootlog_info:    BootLogInfo    = bootlog_info

        self._index_dir:      str = self._bootlog_info.keys_path
        self._index_filepath: str = os.path.join( self._index_dir, f"{self.key}.index" )
        self._keyindex_id:    str = f"{self._bootlog_info.schema_bootid}@{key_info.key}"

        self.index_type:   KeyIndexType  = KeyIndexType.Undetermined
        self.index_state: KeyIndexState = KeyIndexState.Uninitialized

        self._maxrec:   float   = 0
        self._keycnt:   float   = 0
        self._refcnt:   float   = 0
        self._isunique: bool  = True

    def is_proc( self ) -> bool:
        return self._isproc

    def id( self ) -> str:
        return f'index-{self.key}'

    def get_index_info( self: Self ) -> keyIndexInfo:
        return keyIndexInfo(
            keyinfo_id=self._keyindex_id,
            key=self.key,
            alias=self.alias,
            index_type=self.index_type,
            index_state=self._index_state,
            hitpct = round( self._refcnt / self._maxrec * 100 ),
            keycnt= int(self._keycnt),
            refcnt= int(self._refcnt),
            unique=self._isunique
        )

    @abstractmethod
    def main_loop( self: Self, queue: mp.Queue, end_event: mp.Event ) -> None:
        pass

    @abstractmethod
    def apply_tocolumn( self: Self ) -> bool:
        pass

    #def dump_sortedstr( self: Self, strdict: SortedDict[str, LineRefList ] ):




