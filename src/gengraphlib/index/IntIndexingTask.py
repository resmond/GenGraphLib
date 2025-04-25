from typing import Self
import threading as th
import multiprocessing as mp

from sortedcontainers import SortedDict

from ..common import LineRefList, KeyType, KeyIndexType, KeyInfo
from ..bootlog.BootLogInfo import BootLogInfo

from .IndexTaskBase import IndexTaskBase

class IntIndexingTask( IndexTaskBase[int] ):
    def __init__( self: Self, key_info: KeyInfo, bootlog_info: BootLogInfo, mainapp_msgqueue: mp.Queue  ) -> None:
        super( IntIndexingTask, self ).__init__(key_info, bootlog_info, mainapp_msgqueue )

        self._type: type = int
        self._keytype: KeyType.KInt
        self.index_type: KeyIndexType = KeyIndexType.IntSorted

        self.sorted_index: SortedDict[int, LineRefList ] = SortedDict[int, LineRefList ]()
        self.thread: th.Thread = th.Thread( target=self.main_loop, name=self.key, args = (self._queue, self._type,) )

    def start(self: Self) -> None:
        self.thread.start()

    def main_loop( self: Self, queue: mp.Queue, val_type: type ) -> None:
        while True:
            rec_num: int
            value: str
            rec_num, value = queue.get()
            self.recv_value( rec_num, value )

            if self._value_cnt % self.status_cnt == 0:
                self.send_status()

    def recv_value( self: Self, rec_num: int, value: str ) -> None:
        try:
            int_value: int = int( value )

            if int_value not in self.sorted_index:
                self.sorted_index[int_value] = LineRefList()

            self.sorted_index[int_value].append( rec_num )

        except ValueError:
            print(f"IntIndexingTask.recv_value - rec_num: {rec_num}  value: {value}")