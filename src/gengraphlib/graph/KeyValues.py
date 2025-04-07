from typing import Self

from sortedcontainers import SortedDict

from .. import KeyValTypes

class LineRefList( list[ int ] ):
    pass

class KeyValueBase[ T: KeyValTypes ]( SortedDict[ T, LineRefList ] ):
    def __init__(self: Self) -> None:
        super().__init__()
        self.unique: bool = True

    def add_value( self: Self, new_value: T, line_num: int ) -> None:
        if new_value not in self:
            self[new_value] = LineRefList()
        else:
            self.unique = False

        self[new_value].append( line_num )

    def __repr__( self: Self ) -> str:
        return f'{{unique:{self.unique}, cnt:{len(self)}'

