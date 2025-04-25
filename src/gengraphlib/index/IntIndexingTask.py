from typing import Self
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
)

from ..bootlog.BootLogInfo import BootLogInfo

from .IndexTaskBase import IndexTaskBase

class IntIndexingTask( IndexTaskBase[int] ):
    def __init__( self: Self, key_info: KeyInfo, bootlog_info: BootLogInfo, app_msgqueue: mp.Queue, end_event: mp.Event ) -> None:
        super( IntIndexingTask, self ).__init__( key_info, bootlog_info, app_msgqueue, end_event )

        self.keytype: KeyType.KInt
        self.index_type: KeyIndexType = KeyIndexType.IntSorted
        self._index_state = KeyIndexState.Running

        self._queue: mp.Queue = mp.Queue()

        self._sorted_index: SortedDict[int, LineRefList ] = SortedDict[int, LineRefList ]()

        self._thread: th.Thread = th.Thread(
            target=self.main_loop,
            name=f"{self.key}-Int-index",
            args=(
                self._queue,
                self._end_event,
            ),
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

                int_value: int = int( value )

                if int_value not in self._sorted_index:
                    self._sorted_index[int_value ] = LineRefList()

                self._sorted_index[int_value ].append( rec_num )

                if self._value_cnt % self.status_cnt == 0:
                    self.send_status()

        except ValueError as valexc:
            print(f"IntIndexing({self.key}:{self.alias}) ValueError: {valexc}   {value}")

        except Exception as exc:
            print(f"IntIndexing({self.key}:{self.alias}) Exception: {exc}   {value}")

