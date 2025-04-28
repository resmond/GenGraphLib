from typing import Self, cast
import threading as th
import multiprocessing as mp

from sortedcontainers import SortedDict

from ..common import (
    LineRefList,
    KeyType,
    KeyIndexType,
    KeyInfo,
    keyIndexInfo,
    KeyIndexState,
    BootLogInfo
)

from .IndexTaskBase import IndexTaskBase

from ..columns import Column, StrColumn, GraphTable

class StrIndexingTask( IndexTaskBase[str] ):

    def __init__( self: Self, key_info: KeyInfo, bootlog_info: BootLogInfo, graph_table: GraphTable, app_msgqueue: mp.Queue, end_event: mp.Event ) -> None:
        super().__init__( key_info, bootlog_info, graph_table, app_msgqueue, end_event )

        self.keytype      = KeyType.KStr
        self.index_type   = KeyIndexType.StrSorted
        self.index_state  = KeyIndexState.Running

        self._queue: mp.Queue = mp.Queue()

        self._keymap: SortedDict[ str, LineRefList ] = SortedDict[str, LineRefList ]()

        self.thread: th.Thread = th.Thread(
            target=self.main_loop,
            name=f"{self.key}-Str-index",
            args = (self._queue, self.end_event,)
        )

    @property
    def queue( self: Self ) -> mp.Queue:
        return self._queue

    def start(self: Self) -> None:
        self.thread.start()

    def main_loop( self: Self, queue: mp.Queue, end_event: mp.Event ) -> None:
        keyindex_info: keyIndexInfo = self.get_index_info()
        self.app_msgqueue.put( keyindex_info )
        print(f'[{self.key}-index]: Started')
        try:
            while True:   #not end_event:
                rec_num, value = queue.get()

                if rec_num == -1:
                    self.apply_tocolumn(int(value))
                    break

                if value not in self._keymap:
                    self.keycnt += 1
                    self._keymap[value ] = LineRefList()
                else:
                    self.isunique = False

                self._keymap[value ].append( rec_num )
                self.refcnt += 1

                if self.refcnt % self.status_cnt == 0:
                    keyindex_info: keyIndexInfo = self.get_index_info()
                    self.app_msgqueue.put( keyindex_info )
                    #print(f'StrIndexing: {keyindex_info}')

        except ValueError as valexc:
            print(f'StrIndexing({self.key}:{self.alias}) ValueError: {valexc}' )

        except Exception as exc:
            print(f'StrIndexing({self.key}:{self.alias}) Exception: {exc}')

        print(f'StrIndexing({self.key}:{self.alias}) Done')

    def apply_tocolumn( self: Self, maxrecnum: int ) -> bool:
        print(f'[{self.key}-index]: StrColumn Applying Data')
        column: Column[bool] = self.graph_table.gettyped_column( self.key )
        if column:
            strcolumn: StrColumn = cast(StrColumn, column)
            return strcolumn.apply_data( self._keymap, int(self.refcnt), maxrecnum )
        else:
            return False




