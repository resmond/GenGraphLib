from typing import Self, cast
import threading as th
import multiprocessing as mp

from sortedcontainers import SortedSet

from ..common import KeyType, KeyInfo, KeyIndexType, KeyIndexState, keyIndexInfo, BootLogInfo
from .IndexTaskBase import IndexTaskBase

from ..graph.GraphColumns import GraphColumns
from ..columns import Column, BoolColumn

class BoolIndexingTask( IndexTaskBase[bool] ):

    def __init__( self: Self, key_info: KeyInfo, bootlog_info: BootLogInfo, app_msgqueue: mp.Queue, end_event: mp.Event ) -> None:
        super( BoolIndexingTask, self ).__init__( key_info, bootlog_info, app_msgqueue, end_event )

        self.keytype      = KeyType.KBool
        self.index_type   = KeyIndexType.BoolDualIntersect
        self.index_state  = KeyIndexState.Running
        self.isunique     = False

        self._queue: mp.Queue = mp.Queue()

        self._pos_set: SortedSet[int] = SortedSet[int]()
        self._neg_set: SortedSet[int] = SortedSet[int]()

        self.thread: th.Thread = th.Thread(
            target=self.main_loop,
            name=f"{self.key}-Bool-index",
            args = (self._queue, self._end_event, )
        )

    @property
    def queue( self: Self ) -> mp.Queue:
        return self._queue

    def start(self: Self) -> None:
        self.thread.start()

    def main_loop( self: Self, queue: mp.Queue, end_event: mp.Event ) -> None:

        keyindex_info: keyIndexInfo = self.get_index_info()
        self._app_msgqueue.put(keyindex_info)
        print(f'[{self.key}-index]: Started')
        try:
            while not end_event:
                rec_num, value = queue.get()

                if rec_num == -1:
                    self.apply_tocolumn()
                    break

                bool_value: bool = bool( value )

                if bool_value:
                    self._pos_set.add( rec_num )
                else:
                    self._neg_set.add( rec_num )

                if self._keycnt % self.status_cnt == 0:
                    self.send_status()

        except ValueError as valexc:
            print(f'BoolIndexing({self.key}:{self.alias}) ValueError: {valexc}' )

        except Exception as exc:
            print(f'BoolIndexing({self.key}:{self.alias}) Exception: {exc}')

    # pos_set: SortedSet[ int ], neg_set: SortedSet[ int ], refcnt: int
    def apply_tocolumn( self: Self ) -> bool:
        print(f'[{self.key}-index]: BoolColumn Applying Data')
        column: Column[bool] = GraphColumns.inst.get_column( self.key )
        if column:
            boolcolumn: BoolColumn = cast(BoolColumn, column)
            return boolcolumn.apply_data( self._pos_set, self._neg_set, self.refcnt )
        else:
            return False


