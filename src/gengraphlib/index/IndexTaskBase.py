from abc import abstractmethod
from typing import Self

import os.path
import multiprocessing as mp

from ..common import KeyValTypes, KeyType, KeyIndexType, keyIndexInfo, KeyIndexState
from ..graph.KeyValSchemaInfo import KeyInfo
from ..proc.TaskLib import TaskBase, IndexTaskInterface
from ..bootlog.BootLogContext import BootLogInfo, BootLogContext

class IndexTaskBase[ T: KeyValTypes ]( TaskBase, IndexTaskInterface ):

    def __init__(self: Self, key_info: KeyInfo, bootlog_info: BootLogInfo ) -> None:
        super(IndexTaskBase,self).__init__( f"{key_info.key}-index" )
        #self.key_def:   KeyDefBase   = key_def
        #self.keyvalues: KeyValues[T] = keyvalues

        self._bootlog_info: BootLogInfo = bootlog_info
        self._bootlog_context: BootLogContext = BootLogContext( bootlog_info )
        self._keytype: KeyType
        self._type: type = type(T)
        self._key_info: KeyInfo = key_info
        self._key:   str = key_info.key
        self._alias: str = key_info.alias
        self._index_type: KeyIndexType = KeyIndexType.Undetermined
        self._index_state: KeyIndexState = KeyIndexState.Uninitialized
        self._keyinfo_id: str = f"{self._bootlog_info.schema_bootid}@{self._key}"
        self._unique_values: int = 0
        self._value_instances: int = 0
        self._all_unique_values: bool = False

        self._queue: mp.Queue = mp.Queue()
        self._index_dir: str = self._bootlog_info.keys_path
        self._index_filepath: str = os.path.join( self._index_dir, f"{self._key}.bin" )

    @property
    def key( self: Self ) -> str:
        return self._key

    @property
    def alias( self: Self ) -> str:
        return self._alias

    @property
    def index_dir( self: Self ) -> str:
        return self._index_dir

    @property
    def index_filepath( self: Self ) -> str:
        return self._index_filepath

    @property
    def queue( self: Self ) -> mp.Queue:
        return self._queue

    def get_index_info( self: Self ) -> keyIndexInfo:
        return keyIndexInfo( keyinfo_id=self._keyinfo_id, index_type=self._index_type, valuecnt =self._unique_values, instancecnt =self._value_instances, unique =self._all_unique_values )

    @abstractmethod
    def main_loop(self: Self, queue: mp.Queue, val_type: type) -> None:
        pass

    def recv_value( self: Self, rec_num: int, value: str ) -> None:
        pass



