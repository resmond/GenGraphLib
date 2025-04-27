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

from ..graph.GraphColumns import GraphColumns

from ..columns import Column, StrColumn

class StrIndexingTask( IndexTaskBase[str] ):

    def __init__( self: Self, key_info: KeyInfo, bootlog_info: BootLogInfo, app_msgqueue: mp.Queue, end_event: mp.Event ) -> None:
        super( StrIndexingTask, self ).__init__( key_info, bootlog_info, app_msgqueue, end_event )

        self.keytype      = KeyType.KStr
        self.index_type   = KeyIndexType.StrSorted
        self.index_state  = KeyIndexState.Running

        self._queue: mp.Queue = mp.Queue()

        self.sorted_index: SortedDict[ str, LineRefList ] = SortedDict[str, LineRefList ]()

        self.thread: th.Thread = th.Thread(
            target=self.main_loop,
            name=f"{self.key}-Str-index",
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

                self._refcnt += 1
                self._maxrec = rec_num

                if value not in self.sorted_index:
                    self._keycnt += 1
                    self.sorted_index[value] = LineRefList()
                else:
                    self._isunique = False

                self.sorted_index[value].append( rec_num )

                if self._instance_cnt % self.status_cnt == 0:
                    keyindex_info: keyIndexInfo = self.get_index_info()
                    self._app_msgqueue.put( keyindex_info )
                    print(f'StrIndexing: {keyindex_info}')

        except ValueError as valexc:
            print(f'StrIndexing({self.key}:{self.alias}) ValueError: {valexc}' )

        except Exception as exc:
            print(f'StrIndexing({self.key}:{self.alias}) Exception: {exc}')

    def apply_tocolumn( self: Self ) -> bool:
        print(f'[{self.key}-index]: StrColumn Applying Data')
        column: Column[str] = GraphColumns.inst.get_column( self.key )
        if column:
            strcolumn: StrColumn = cast(StrColumn, column)
            return strcolumn.apply_data( self.keymap, self.refcnt )
        else:
            return False




