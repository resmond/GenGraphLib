from typing import Self

from sortedcontainers import SortedDict

from .KeyValues import KeyValues
from ..common import KeyDefInterface, LineRefList

class IntKeyValueSet( KeyValues[int] ):
    def __init__( self: Self, _key_def: KeyDefInterface ) -> None:
        super(IntKeyValueSet, self).__init__( _key_def )

        self.fields: SortedDict[int, LineRefList] = SortedDict[int, LineRefList]()


