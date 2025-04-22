from typing import Self
from ..common import LineRefList

from sortedcontainers import SortedDict

from IndexTaskBase import IndexTaskBase

class StrIndexingTask( IndexTaskBase[str] ):
    def __init__( self: Self, key: str, alias: str, root_dir: str  ) -> None:
        super( StrIndexingTask, self ).__init__(key, alias, root_dir)
        self.sorted_index: SortedDict[str, LineRefList ] = SortedDict[str, LineRefList ]()

    def recv_value( self: Self, rec_num: int, buffer: bytes ) -> None:
        str_value: str = buffer.decode()

        if str_value not in self.sorted_index:
            self.sorted_index[str_value] = LineRefList()

        self.sorted_index[str_value].append( rec_num )

