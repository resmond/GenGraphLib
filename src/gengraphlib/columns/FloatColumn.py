from typing import Self

from sortedcontainers import SortedDict

from .KeyValues import KeyValues
from ..common import KeyDefInterface, LineRefList

class FloatKeyValueSet( KeyValues[float] ):
    def __init__( self: Self, _key_def: KeyDefInterface ) -> None:
        super(FloatKeyValueSet, self).__init__( _key_def )

        self.fields: SortedDict[float, LineRefList] = SortedDict[float, LineRefList]()

