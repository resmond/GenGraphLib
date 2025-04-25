from typing import Self
import threading as th
import multiprocessing as mp

from sortedcontainers import SortedDict

from ..common import LineRefList, KeyType, KeyIndexType, KeyInfo, keyIndexInfo, KeyIndexState

from ..bootlog.BootLogInfo import BootLogInfo
from .IndexTaskBase import IndexTaskBase

class StrIndexingTask( IndexTaskBase[str] ):
    def __init__( self: Self, key_info: KeyInfo, bootlog_info: BootLogInfo, app_msgqueue: mp.Queue, end_event: mp.Event ) -> None:
        super( StrIndexingTask, self ).__init__( key_info, bootlog_info, app_msgqueue, end_event )

        self.keytype      = KeyType.KStr
        self.index_type   = KeyIndexType.StrSorted
        self._index_state = KeyIndexState.Running

        self._queue: mp.Queue = mp.Queue()

        self._sorted_index: SortedDict[str, LineRefList ] = SortedDict[str, LineRefList ]()
        self._thread: th.Thread = th.Thread(
            target=self.main_loop,
            name=f"{self.key}-Str-index",
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

        rec_num: int = 0
        value: str = ""
        try:
            while not end_event:

                rec_num, value = queue.get()

                if value not in self._sorted_index:
                    self._sorted_index[value] = LineRefList()
                else:
                    self._is_unique = False

                self._sorted_index[value].append( rec_num )

                if self._instance_cnt % self.status_cnt == 0:
                    keyindex_info: keyIndexInfo = self.get_index_info()
                    self._app_msgqueue.put( keyindex_info )

        except ValueError as valexc:
            print(f'StrIndexing({self.key}:{self.alias}) ValueError: {valexc}   {value}' )

        except Exception as exc:
            print(f'StrIndexing({self.key}:{self.alias}) Exception: {exc}   {value}')

