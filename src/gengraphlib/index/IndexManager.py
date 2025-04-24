from typing import Self

import multiprocessing as mp

from ..common import KeyValTypes, KeyType, KeyValSchemaInfo

from ..bootlog import BootLogInfo
from ..proc.TaskLib import IndexTaskInterface, IndexManagerInterface

from .StrIndexingTask import StrIndexingTask
from .IntIndexingTask import IntIndexingTask
from .BoolIndexingTask import BoolIndexingTask
from .FloatIndexingTask import FloatIndexingTask
from .TmstIndexingTask import TmstIndexingTask


class IndexManager[ T: KeyValTypes ]( IndexManagerInterface ):

    def __init__( self: Self, keyval_schema_info: KeyValSchemaInfo ) -> None:
        super( IndexManager, self ).__init__()

        self.keyvalue_schema_info: KeyValSchemaInfo = keyval_schema_info
        self._bootlog_info: BootLogInfo | None = None

        self.index_queuemap: dict[str, mp.Queue] = dict[str, mp.Queue]()
        self.index_taskmap: dict[str, IndexTaskInterface] = dict[str, IndexTaskInterface]()

        self.active_keys: set[str] | None = None
        self.state: str = "Init"

    def register_index( self: Self, index: IndexTaskInterface ) -> None:
        self.index_queuemap[index.alias] = index.queue
        self.index_taskmap[index.id()] = index

    def start_indexes( self: Self,  bootlog_info: BootLogInfo, active_keys: set[str] ) -> dict[str, mp.Queue ]:
        self._bootlog_info = bootlog_info
        self.active_keys = active_keys
        for keyinfo in self.keyvalue_schema_info.keys:
            if keyinfo.alias in self.active_keys:
                match keyinfo.keytype:
                    case KeyType.KStr:
                        self.register_index( StrIndexingTask( keyinfo, self._bootlog_info ) )
                    case KeyType.KInt:
                        self.register_index( IntIndexingTask( keyinfo, self._bootlog_info ) )
                    case KeyType.KBool:
                        self.register_index( BoolIndexingTask( keyinfo, self._bootlog_info ) )
                    case KeyType.KFloat:
                        self.register_index( FloatIndexingTask( keyinfo, self._bootlog_info ) )
                    case KeyType.KTmst:
                        self.register_index( TmstIndexingTask( keyinfo, self._bootlog_info ) )

        for index in self.index_taskmap.values():
            index.start()

        self.state = "indexes-started"

        return self.index_queuemap

    def stop_indexes(self: Self) -> None:
        for index in self.index_taskmap.values():
            index.stop()

    # def start_indexes(self: Self) -> None:
    #     for index in self.index_taskmap.values():
    #         index.start()


    def getqueues_byalias( self: Self ) -> dict[str, mp.Queue ]:
        _queues_byalias: dict[str, mp.Queue] = dict[str, mp.Queue ]()

        for key, queue in self.index_queuemap.items():
            _queues_byalias[key] = queue

        self.state = "bound to valve-pump"
        return _queues_byalias




