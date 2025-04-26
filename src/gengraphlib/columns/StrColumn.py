from typing import Self

from sortedcontainers import SortedDict

from ..common import KeyDefInterface, LineRefList

from .Column import Column

class StrColumn( Column[str ] ):
    def __init__( self: Self, _key_def: KeyDefInterface ) -> None:
        super( StrColumn, self ).__init__( _key_def )

        self.fields: SortedDict[str, LineRefList] = SortedDict[str, LineRefList]()

