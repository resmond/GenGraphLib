from typing import Self, cast
import threading as th
import multiprocessing as mp

from sortedcontainers import SortedDict

from ..common import (
    LineRefList,
    KeyType,
    KeyIndexType,
    KeyInfo,
    KeyIndexState,
    keyIndexInfo,
    BootLogInfo
)

from .IndexTaskBase import IndexTaskBase


from ..columns import Column, IntColumn
from ..graphs import GraphTable

class IntIndexingTask( IndexTaskBase[int] ):
    def __init__( self: Self, key_info: KeyInfo, bootlog_info: BootLogInfo, graph_table: GraphTable, app_msgqueue: mp.Queue, end_event: mp.Event ) -> None:
        super().__init__( key_info, bootlog_info, graph_table, app_msgqueue, end_event )

        self.keytype: KeyType.KInt
        self.index_type: KeyIndexType = KeyIndexType.IntSorted
        self._index_state = KeyIndexState.Running

        self._queue: mp.Queue = mp.Queue()

        self._keymap: SortedDict[int, LineRefList ] = SortedDict[int, LineRefList ]()

        self._thread: th.Thread = th.Thread(
            target=self.main_loop,
            name=f"{self.key}-Int-index",
            args=(
                self._queue,
                self.end_event,
            ),
        )

    @property
    def queue( self: Self ) -> mp.Queue:
        return self._queue

    def start(self: Self) -> None:
        self._thread.start()

    def main_loop( self: Self, queue: mp.Queue, end_event: mp.Event ) -> None:
        keyindex_info: keyIndexInfo = self.get_index_info()
        self.app_msgqueue.put( keyindex_info )

        try:
            while not end_event:
                rec_num, value = queue.get()

                if rec_num == -1:
                    self.apply_tocolumn(int(value))
                    break

                int_value: int = int( value )

                if int_value not in self._keymap:
                    self.keycnt += 1
                    self._keymap[int_value ] = LineRefList()

                self._keymap[int_value ].append( rec_num )
                self.refcnt += 1

                if self.refcnt % self.status_cnt == 0:
                    self.send_status()

        except ValueError as valexc:
            print(f'IntIndexing({self.key}:{self.alias}) ValueError: {valexc}')

        except Exception as exc:
            print(f'IntIndexing({self.key}:{self.alias}) Exception: {exc}')

    def apply_tocolumn( self: Self, maxrecnum: int ) -> bool:
        print(f'[{self.key}-index]: IntColumn Applying Data')
        column: Column[bool] = self.graph_table.gettyped_column( self.key )
        if column:
            intcolumn: IntColumn = cast(IntColumn, column)
            return intcolumn.apply_data( self._keymap, int( self.refcnt ), maxrecnum )
        else:
            return False
