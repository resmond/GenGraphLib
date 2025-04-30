from typing import Self, cast

import pyarrow as par

from sortedcontainers import SortedSet

from ..common import KeyInfo, LineRefList

from .Column import Column

class BoolColumn( Column[bool] ):
    def __init__( self: Self, keyinfo: KeyInfo, datadir: str, load_data: bool = False ) -> None:
        super( BoolColumn, self ).__init__( keyinfo, datadir, load_data )

        self.refcnt:      int = -1
        self.maxrecnum:   int = -1
        self.keyvaluecnt: int = 2
        self.pos_set: SortedSet[ int ] = SortedSet[ int ]()
        self.neg_set: SortedSet[ int ] = SortedSet[ int ]()

    def apply_data( self: Self, pos_set: SortedSet[ int ], neg_set: SortedSet[ int ], refcnt: int, maxrecnum: int, skip_write: bool = False ) -> bool:
        try:

            self.refcnt    = refcnt
            self.maxrecnum = maxrecnum
            self.pos_set   = pos_set
            self.neg_set   = neg_set

            if not skip_write:
                self.write_file()

            self.wr

            return True

        except Exception as exc:
            print(f"BoolColumn[{self.id}].apply_data() - Exception: {exc}")
            return False

    def keyvalue_from_recno( self: Self, recno: int ) -> bool | None:
        if recno in self.pos_set:
            return True
        elif recno in self.neg_set:
            return False
        else:
            return None

    def keyvalue_from_valueindex( self: Self, valueindex: int ) -> bool | None:
        return not valueindex == 0

    def valueindex_from_recno( self: Self, recno: int ) -> int | None:
        return int( recno in self.pos_set )

    def valueindex_from_keyvalue( self: Self, keyvalue: bool ) -> int | None:
        return int( keyvalue )

    def refs_from_keyvalue( self: Self, keyvalue: bool ) -> LineRefList | None:
        if keyvalue:
            return cast( list, self.pos_set )
        else:
            return cast( list, self.neg_set )

    def refs_from_valueindex( self: Self, valueindex: int ) -> LineRefList | None:
        if valueindex == 0:
            return cast( list, self.pos_set )
        else:
            return cast( list, self.neg_set )

    def apply_objdata( self: Self, objdata: Self ) -> bool:

        self.refcnt      = objdata.refcnt
        self.keyvaluecnt = objdata.keyvaluecnt
        self.pos_set     = objdata.pos_set
        self.neg_set     = objdata.neg_set

        return True

    def get_arrowdata( self: Self ) -> tuple[par.DataType, list[ bool | None ], bool ]:
        neg_high: int = self.neg_set.index(len(self.neg_set)-1)
        pos_high: int = self.pos_set.index(len(self.pos_set)-1)
        maxref: int = max(neg_high, pos_high)
        col_array = list[ bool | None ]()

        for row in range(0, maxref):
            value: bool | None = None
            if row in self.pos_set:
                value = True
            elif row in self.neg_set:
                value = False
            col_array.append( value )

        return par.bool_(), col_array, False


