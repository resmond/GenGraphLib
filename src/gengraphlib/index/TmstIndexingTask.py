from typing import Self, cast
import threading as th
import multiprocessing as mp

import datetime as dt

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


from ..columns import Column, TmstColumn, GraphTable

# noinspection DuplicatedCode
class TmstIndexingTask( IndexTaskBase[dt.datetime] ):

    def __init__( self: Self, key_info: KeyInfo, bootlog_info: BootLogInfo, graph_table: GraphTable, app_msgqueue: mp.Queue, end_event: mp.Event ) -> None:
        super( TmstIndexingTask, self ).__init__( key_info, bootlog_info, graph_table, app_msgqueue, end_event )

        self.keytype      = KeyType.KTmst
        self.index_type   = KeyIndexType.TmstSorted
        self._index_state = KeyIndexState.Running
        self._is_unique   = False

        self._queue: mp.Queue = mp.Queue()

        self._keymap: SortedDict[dt.datetime, LineRefList ] = SortedDict[dt.datetime, LineRefList ]()

        self._thread: th.Thread = th.Thread(
            target=self.main_loop,
            name=f"{self.key}-Tmst-index",
            args = (self._queue, self.end_event,)
        )

    @property
    def queue( self: Self ) -> mp.Queue:
        return self._queue

    def start(self: Self) -> None:
        self._thread.start()

    def main_loop( self: Self, queue: mp.Queue, end_event: mp.Event ) -> None:
        very_beginning = dt.datetime.fromisoformat("1970-01-01")

        keyindex_info: keyIndexInfo = self.get_index_info()
        self.app_msgqueue.put( keyindex_info )

        try:
            while True: #not end_event:
                rec_num, value = queue.get()

                if rec_num == -1:
                    self.apply_tocolumn(int(value))
                    break

                int_value = int(value)
                datetime_value: dt.datetime = very_beginning + dt.timedelta(microseconds=int_value)

                if datetime_value not in self._keymap:
                    self.keycnt += 1
                    self._keymap[datetime_value ] = LineRefList()

                self._keymap[datetime_value ].append( rec_num )
                self.refcnt += 1

                if self.refcnt % self.status_cnt == 0:
                    keyindex_info: keyIndexInfo = self.get_index_info()
                    #print(f"TmstIndexing({self.key}:{self.alias}) {self.refcnt}" )
                    self.app_msgqueue.put( keyindex_info )

        except ValueError as valexc:
            print(f'TmstIndexing({self.key}:{self.alias}) ValueError: {valexc}' )

        except Exception as exc:
            print(f'TmstIndexing({self.key}:{self.alias}) Exception: {exc}')

        print(f'TmstIndexing({self.key}:{self.alias}) Done')

    def apply_tocolumn( self: Self, maxrecnum: int ) -> bool:
        print(f'[{self.key}-index]: TmstColumn Applying Data')
        column: Column[bool] = self.graph_table.gettyped_column( self.key )
        if column:
            tmstcolumn: TmstColumn = cast(TmstColumn, column)
            return tmstcolumn.apply_data( self._keymap, int( self.refcnt ), maxrecnum )
        else:
            return False
