from typing import Self
from ..common import LineRefList

from sortedcontainers import SortedDict

from IndexTaskBase import IndexTaskBase

class IntIndexingTask( IndexTaskBase[int] ):
    def __init__( self: Self, key: str, alias: str, root_dir: str  ) -> None:
        super( IntIndexingTask, self ).__init__(key, alias, root_dir)
        self.sorted_index: SortedDict[int, LineRefList ] = SortedDict[int, LineRefList ]()

    def recv_value( self: Self, rec_num: int, buffer: bytes ) -> None:
        str_value: str = buffer.decode()
        int_value: int = int( str_value )

        if int_value not in self.sorted_index:
            self.sorted_index[int_value] = LineRefList()

        self.sorted_index[int_value].append( rec_num )
