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

from ..graph.GraphColumns import GraphColumns

from ..columns import Column, FloatColumn

# noinspection DuplicatedCode
class FloatIndexingTask( IndexTaskBase[float] ):
    def __init__( self: Self, key_info: KeyInfo, bootlog_info: BootLogInfo, app_msgqueue: mp.Queue, end_event: mp.Event ) -> None:
        super( FloatIndexingTask, self ).__init__( key_info, bootlog_info, app_msgqueue, end_event )

        self._keytype     = KeyType.KFloat
        self.index_type   = KeyIndexType.FloatSorted
        self._index_state = KeyIndexState.Running

        self._queue: mp.Queue = mp.Queue()

        self._sorted_index: SortedDict[float, LineRefList ] = SortedDict[float, LineRefList ]()

        self._thread: th.Thread = th.Thread(
            target=self.main_loop,
            name=f"{self.key}-Float-index",
            args = (self._queue, self._end_event, )
        )

    @property
    def queue( self: Self ) -> mp.Queue:
        return self._queue

    def start(self: Self) -> None:
        self._thread.start()

    def main_loop( self: Self, queue: mp.Queue, end_event: mp.Event ) -> None:
        keyindex_info: keyIndexInfo = self.get_index_info()
        self._app_msgqueue.put(keyindex_info)

        try:
            while True:
                rec_num, value = queue.get()

                if rec_num == -1:
                    self.apply_tocolumn()
                    break

                float_value: float = float( value )

                if float_value not in self._sorted_index:
                    self._sorted_index[float_value] = LineRefList()

                self._sorted_index[float_value].append( rec_num )

                if self._instance_cnt % self.status_cnt == 0:
                    keyindex_info: keyIndexInfo = self.get_index_info()
                    self._app_msgqueue.put( keyindex_info )

        except ValueError as valexc:
            print(f'FloatIndexing({self.key}:{self.alias}) ValueError: {valexc}' )

        except Exception as exc:
            print(f'FloatIndexing({self.key}:{self.alias}) Exception: {exc}')

    def apply_tocolumn( self: Self ) -> bool:
        print(f'[{self.key}-index]: FloatColumn Applying Data')
        column: Column[float] = GraphColumns.inst.get_column( self.key )
        if column:
            floatcolumn: FloatColumn = cast(FloatColumn, column)
            return floatcolumn.apply_data( self.keymap, self.refcnt )
        else:
            return False
