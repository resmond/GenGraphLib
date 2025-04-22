from typing import Self
from ..common import LineRefList

from sortedcontainers import SortedDict

from IndexTaskBase import IndexTaskBase

class FloatIndexingTask( IndexTaskBase[float] ):
    def __init__( self: Self, key: str, alias: str, root_dir: str  ) -> None:
        super( FloatIndexingTask, self ).__init__(key, alias, root_dir)
        self.sorted_index: SortedDict[float, LineRefList ] = SortedDict[float, LineRefList ]()

    def recv_value( self: Self, rec_num: int, buffer: bytes ) -> None:
        str_value: str = buffer.decode()
        float_value: float = float( str_value )

        if float_value not in self.sorted_index:
            self.sorted_index[float_value] = LineRefList()

        self.sorted_index[float_value].append( rec_num )
