from typing import Self
import threading as th
import multiprocessing as mp

from sortedcontainers import SortedDict

from ..common import LineRefList, KeyType, KeyIndexType, KeyInfo
from ..bootlog.BootLogInfo import BootLogInfo
from .IndexTaskBase import IndexTaskBase

class StrIndexingTask( IndexTaskBase[str] ):
    def __init__( self: Self, key_info: KeyInfo, bootlog_info: BootLogInfo, mainapp_msgqueue: mp.Queue  ) -> None:
        super( StrIndexingTask, self ).__init__(key_info, bootlog_info, mainapp_msgqueue )

        self._type: type = str
        self._keytype: KeyType.KStr
        self.index_type: KeyIndexType = KeyIndexType.StrSorted

        self.sorted_index: SortedDict[str, LineRefList ] = SortedDict[str, LineRefList ]()
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
            if value not in self.sorted_index:
                self.sorted_index[value] = LineRefList()

            self.sorted_index[value].append( rec_num )

        except ValueError:
            print(f"StrIndexingTask.recv_value - rec_num: {rec_num}  value: {value}")
