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
    KeyInfo
)
from ..proc.TaskLib import TaskBase, IndexTaskInterface
from ..bootlog.BootLogContext import BootLogInfo, BootLogContext

class IndexTaskBase[ T: KeyValTypes ]( TaskBase, IndexTaskInterface ):

    def __init__( self: Self, key_info: KeyInfo, bootlog_info: BootLogInfo, app_msgqueue: mp.Queue, end_event: mp.Event ) -> None:
        super(IndexTaskBase,self).__init__( f"{key_info.key}-index" )

        self.status_cnt: int     = 100
        self.key:        str     = key_info.key
        self.alias:      str     = key_info.alias
        self.key_info:   KeyInfo = key_info
        self.keytype:    KeyType = key_info.keytype

        self._app_msgqueue:    mp.Queue       = app_msgqueue
        self._end_event:       mp.Event       = end_event

        self._bootlog_info:    BootLogInfo    = bootlog_info
        self._bootlog_context: BootLogContext = BootLogContext( bootlog_info )

        self._index_dir:      str = self._bootlog_info.keys_path
        self._index_filepath: str = os.path.join( self._index_dir, f"{self.key}.index" )
        self._keyindex_id:    str = f"{self._bootlog_info.schema_bootid}@{key_info.key}"

        self.index_type:   KeyIndexType = KeyIndexType.Undetermined
        self._index_state: KeyIndexState = KeyIndexState.Uninitialized

        self._value_cnt:     int = 0
        self._instances_cnt: int = 0
        self._is_unique:     bool = True

    def get_index_info( self: Self ) -> keyIndexInfo:
        return keyIndexInfo(
            keyinfo_id=self._keyindex_id,
            key=self.key,
            alias=self.alias,
            index_type=self.index_type,
            valuecnt=self._value_cnt,
            instancecnt=self._instances_cnt,
            unique=self._is_unique
        )

    @abstractmethod
    def main_loop( self: Self, queue: mp.Queue, end_event: mp.Event ) -> None:
        pass




