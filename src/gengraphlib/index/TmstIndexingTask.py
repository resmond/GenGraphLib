from typing import Self
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


# noinspection DuplicatedCode
class TmstIndexingTask( IndexTaskBase[dt.datetime] ):

    def __init__( self: Self, key_info: KeyInfo, bootlog_info: BootLogInfo, app_msgqueue: mp.Queue, end_event: mp.Event ) -> None:
        super( TmstIndexingTask, self ).__init__( key_info, bootlog_info, app_msgqueue, end_event )

        self.keytype      = KeyType.KTmst
        self.index_type   = KeyIndexType.TmstSorted
        self._index_state = KeyIndexState.Running
        self._is_unique   = False

        self._queue: mp.Queue = mp.Queue()

        self.sorted_index: SortedDict[dt.datetime, LineRefList ] = SortedDict[dt.datetime, LineRefList ]()

        self._thread: th.Thread = th.Thread(
            target=self.main_loop,
            name=f"{self.key}-Tmst-index",
            args = (self._queue, self._end_event, )
        )

    @property
    def queue( self: Self ) -> mp.Queue:
        return self._queue

    def start(self: Self) -> None:
        self._thread.start()

    def main_loop( self: Self, queue: mp.Queue, end_event: mp.Event ) -> None:
        very_beginning = dt.datetime.fromisoformat("1970-01-01")

        keyindex_info: keyIndexInfo = self.get_index_info()
        self._app_msgqueue.put(keyindex_info)

        try:
            while not end_event:
                rec_num, value = queue.get()

                int_value = int(value)
                datetime_value: dt.datetime = very_beginning + dt.timedelta(microseconds=int_value)

                if datetime_value not in self.sorted_index:
                    self.sorted_index[datetime_value] = LineRefList()

                self.sorted_index[datetime_value].append(rec_num)

                if self._keycnt % self.status_cnt == 0:
                    keyindex_info: keyIndexInfo = self.get_index_info()
                    self._app_msgqueue.put(keyindex_info)

        except ValueError as valexc:
            print(f'TmstIndexing({self.key}:{self.alias}) ValueError: {valexc}' )

        except Exception as exc:
            print(f'TmstIndexing({self.key}:{self.alias}) Exception: {exc}')

    def serialize_index( self: Self ):
        pass
