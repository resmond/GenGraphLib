from typing import Self

from sortedcontainers import SortedDict

from .KeyValues import KeyValues
from ..common import KeyDefInterface, LineRefList

class StrKeyValueSet( KeyValues[str] ):
    def __init__( self: Self, _key_def: KeyDefInterface ) -> None:
        super(StrKeyValueSet, self).__init__( _key_def )

        self.fields: SortedDict[str, LineRefList] = SortedDict[str, LineRefList]()

