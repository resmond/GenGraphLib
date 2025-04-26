from typing import Self

from sortedcontainers import SortedSet

from ..common import KeyDefInterface

from .Column import Column

class BoolColumn( Column[bool ] ):
    def __init__( self: Self, _key_def: KeyDefInterface ) -> None:
        super( BoolColumn, self ).__init__( _key_def )

        self.positive: SortedSet[int] = SortedSet[int]()
        self.negative: SortedSet[int] = SortedSet[int]()

