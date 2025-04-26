from typing import Self

import datetime as dt

from sortedcontainers import SortedDict

from .KeyValues import KeyValues
from ..common import KeyDefInterface, LineRefList

class TmstKeyValueSet( KeyValues[dt.datetime] ):
    def __init__( self: Self, _key_def: KeyDefInterface ) -> None:
        super(TmstKeyValueSet, self).__init__( _key_def )

        self.fields: SortedDict[dt.datetime, LineRefList] = SortedDict[dt.datetime, LineRefList]()


