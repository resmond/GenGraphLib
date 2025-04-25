from typing import Self
import threading as th
import multiprocessing as mp

from sortedcontainers import SortedSet

from ..common import KeyType, KeyInfo, KeyIndexType, KeyIndexState, keyIndexInfo
from ..bootlog.BootLogInfo import BootLogInfo
from .IndexTaskBase import IndexTaskBase

class BoolIndexingTask( IndexTaskBase[bool] ):

    def __init__( self: Self, key_info: KeyInfo, bootlog_info: BootLogInfo, app_msgqueue: mp.Queue, end_event: mp.Event ) -> None:
        super( BoolIndexingTask, self ).__init__( key_info, bootlog_info, app_msgqueue, end_event )

        self.keytype      = KeyType.KBool
        self.index_type   = KeyIndexType.BoolDualIntersect
        self._index_state = KeyIndexState.Running
        self._is_unique   = False

        self._queue: mp.Queue = mp.Queue()

        self._positive_intersection: SortedSet[int ] = SortedSet[int ]()
        self._negative_intersectio:  SortedSet[int ] = SortedSet[int ]()

        self._thread: th.Thread = th.Thread(
            target=self.main_loop,
            name=f"{self.key}-Bool-index",
            args = (self._queue, self._end_event, )
        )

    @property
    def queue( self: Self ) -> mp.Queue:
        return self._queue

    def start(self: Self) -> None:
        self._thread.start()

    def main_loop( self: Self, queue: mp.Queue, end_event: mp.Event ) -> None:
        rec_num: int = 0
        value: str = ""

        keyindex_info: keyIndexInfo = self.get_index_info()
        self._app_msgqueue.put(keyindex_info)

        try:
            while not end_event:
                rec_num, value = queue.get()

                bool_value: bool = bool( value )

                if bool_value:
                    self._positive_intersection.add( rec_num )
                else:
                    self._negative_intersection.add( rec_num )

                if self._value_cnt % self.status_cnt == 0:
                    self.send_status()

        except ValueError as valexc:
            print(f'BoolIndexing({self.key}:{self.alias}) ValueError: {valexc}   {value}' )

        except Exception as exc:
            print(f'BoolIndexing({self.key}:{self.alias}) Exception: {exc}   {value}')



