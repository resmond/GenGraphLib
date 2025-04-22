from typing import Self

import datetime as dt

from sortedcontainers import SortedDict

from IndexTaskBase import IndexTaskBase
from src.gengraphlib import LineRefList

class TmstIndexingTask( IndexTaskBase[dt.datetime] ):
    very_beginning = dt.datetime.fromisoformat("1970-01-01")

    def __init__( self: Self, key: str, alias: str, root_dir: str  ) -> None:
        super( TmstIndexingTask, self ).__init__(key, alias, root_dir)
        self.sorted_index: SortedDict[dt.datetime, LineRefList ] = SortedDict[dt.datetime, LineRefList ]()

    def recv_value( self: Self, rec_num: int, buffer: bytes ) -> None:
        try:
            str_value: str = buffer.decode()
            int_value = int(str_value)
            datetime_value: dt.datetime = TmstIndexingTask.convert_to_datetime(int_value)

            if datetime_value not in self.sorted_index:
                self.sorted_index[datetime_value] = LineRefList()

            self.sorted_index[datetime_value].append(rec_num)

        except ValueError as valexc:
            print( f'[TmstIndexingTask.recv_value({self._key}:{self._alias})] ValueError: {valexc} - "{buffer.hex()}"' )

        except Exception as exc:
            print( f'[TmstIndexingTask.recv_value({self._key}:{self._alias})] Exception: {exc} - "{buffer.hex()}"' )

    @staticmethod
    def convert_to_datetime( microsec_offset: int ) -> dt.datetime:
        return TmstIndexingTask.very_beginning + dt.timedelta( microseconds=microsec_offset )

