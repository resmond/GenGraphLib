from typing import Self

from sortedcontainers import SortedSet

from .KeyValues import KeyValues
from ..common import KeyDefInterface

class BoolKeyValueSet( KeyValues[bool] ):
    def __init__( self: Self, _key_def: KeyDefInterface ) -> None:
        super(BoolKeyValueSet, self).__init__( _key_def )

        self.positive: SortedSet[int] = SortedSet[int]()
        self.negative: SortedSet[int] = SortedSet[int]()

