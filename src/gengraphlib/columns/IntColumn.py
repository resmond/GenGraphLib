from typing import Self

from sortedcontainers import SortedDict

from ..common import KeyDefInterface, LineRefList

from .Column import Column

class IntColumn( Column[int ] ):
    def __init__( self: Self, _key_def: KeyDefInterface ) -> None:
        super( IntColumn, self ).__init__( _key_def )

        self.fields: SortedDict[int, LineRefList] = SortedDict[int, LineRefList]()


