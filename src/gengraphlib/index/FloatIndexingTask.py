from typing import Self
import threading as th
import multiprocessing as mp

from sortedcontainers import SortedDict

from ..common import LineRefList, KeyType, KeyIndexType
from ..graph.KeyValSchemaInfo import KeyInfo
from ..bootlog.BootLogInfo import BootLogInfo

from .IndexTaskBase import IndexTaskBase

class FloatIndexingTask( IndexTaskBase[float] ):
    def __init__( self: Self, key_info: KeyInfo, bootlog_info: BootLogInfo  ) -> None:
        super( FloatIndexingTask, self ).__init__(key_info, bootlog_info )

        self._type: type = float
        self._keytype: KeyType.KFloat
        self.index_type: KeyIndexType = KeyIndexType.FloatSorted

        self.sorted_index: SortedDict[float, LineRefList ] = SortedDict[float, LineRefList ]()
        self.thread: th.Thread = th.Thread(target=self.main_loop, name=self._key, args = (self._queue, self._type, ) )

    def start( self: Self ) -> None:
        self.thread.start()

    def main_loop( self: Self, queue: mp.Queue, val_type: type ) -> None:
        while True:
            rec_num: int
            value: str
            rec_num, value = queue.get()
            self.recv_value( rec_num, value )

    def recv_value( self: Self, rec_num: int, value: str ) -> None:
        try:
            float_value: float = float( value )

            if float_value not in self.sorted_index:
                self.sorted_index[float_value] = LineRefList()

            self.sorted_index[float_value].append( rec_num )
            
        except ValueError:
            print(f"FloatIndexingTask.recv_value - rec_num: {rec_num}  value: {value}")
