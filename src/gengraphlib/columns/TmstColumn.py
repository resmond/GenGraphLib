from typing import Self

import datetime as dt

from sortedcontainers import SortedDict

from ..common import KeyDefInterface, LineRefList

from .Column import Column

class TmstColumn( Column[dt.datetime ] ):
    def __init__( self: Self, _key_def: KeyDefInterface ) -> None:
        super( TmstColumn, self ).__init__( _key_def )

        self.fields: SortedDict[dt.datetime, LineRefList] = SortedDict[dt.datetime, LineRefList]()


