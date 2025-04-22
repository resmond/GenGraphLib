from typing import Self
from ..common import LineRefList

from sortedcontainers import SortedDict

from .IndexTaskBase import IndexTaskBase

class IntIndexingTask( IndexTaskBase[int] ):
    def __init__( self: Self, key: str, alias: str, root_dir: str  ) -> None:
        super( IntIndexingTask, self ).__init__(key, alias, root_dir)
        self.sorted_index: SortedDict[int, LineRefList ] = SortedDict[int, LineRefList ]()

    def recv_value( self: Self, rec_num: int, value: str ) -> None:

        try:
            int_value: int = int( value )

            if int_value not in self.sorted_index:
                self.sorted_index[int_value] = LineRefList()

            self.sorted_index[int_value].append( rec_num )

        except ValueError:
            print(f"IntIndexingTask.recv_value - rec_num: {rec_num}  value: {value}")