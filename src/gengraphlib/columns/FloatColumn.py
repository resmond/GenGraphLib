from typing import Self

from sortedcontainers import SortedDict

from ..common import KeyDefInterface, LineRefList

from .Column import Column

class FloatColumn( Column[float ] ):
    def __init__( self: Self, _key_def: KeyDefInterface ) -> None:
        super( FloatColumn, self ).__init__( _key_def )

        self.fields: SortedDict[float, LineRefList] = SortedDict[float, LineRefList]()

