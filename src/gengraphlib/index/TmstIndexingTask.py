from typing import Self
import threading as th
import multiprocessing as mp

import datetime as dt

from sortedcontainers import SortedDict

from ..common import LineRefList, KeyType, KeyIndexType, KeyInfo
from ..bootlog.BootLogInfo import BootLogInfo

from .IndexTaskBase import IndexTaskBase

class TmstIndexingTask( IndexTaskBase[dt.datetime] ):
    very_beginning = dt.datetime.fromisoformat("1970-01-01")

    def __init__( self: Self, key_info: KeyInfo, bootlog_info: BootLogInfo  ) -> None:
        super( TmstIndexingTask, self ).__init__(key_info, bootlog_info )

        self._type: type = dt.datetime
        self._keytype: KeyType.KTmst
        self.index_type: KeyIndexType = KeyIndexType.TmstSorted

        self.sorted_index: SortedDict[dt.datetime, LineRefList ] = SortedDict[dt.datetime, LineRefList ]()
        self.thread: th.Thread = th.Thread( target=self.main_loop, name=self.key, args = (self._queue, self._type,) )

    def start(self: Self) -> None:
        self.thread.start()

    def main_loop( self: Self, queue: mp.Queue, val_type: type ) -> None:
        while True:
            rec_num: int
            value: str
            rec_num, value = queue.get()
            self.recv_value( rec_num, value )

    def recv_value( self: Self, rec_num: int, value: str ) -> None:
        try:
            int_value = int(value)
            datetime_value: dt.datetime = TmstIndexingTask.convert_to_datetime(int_value)

            if datetime_value not in self.sorted_index:
                self.sorted_index[datetime_value] = LineRefList()

            self.sorted_index[datetime_value].append(rec_num)

        except ValueError as valexc:
            print( f'[TmstIndexingTask.recv_value({self.key}:{self.alias})] ValueError: {valexc} - "{value}"' )

        except Exception as exc:
            print( f'[TmstIndexingTask.recv_value({self.key}:{self.alias})] Exception: {exc} - "{value}"' )

    @staticmethod
    def convert_to_datetime( microsec_offset: int ) -> dt.datetime:
        return TmstIndexingTask.very_beginning + dt.timedelta( microseconds=microsec_offset )

