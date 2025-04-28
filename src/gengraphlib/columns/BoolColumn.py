from typing import Self, cast

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

    def apply_load( self: Self, dataobj: Self ) -> bool:

        self.refcnt      = dataobj.refcnt
        self.keyvaluecnt = dataobj.keyvaluecnt
        self.pos_set     = dataobj.pos_set
        self.neg_set     = dataobj.neg_set

        return True

    # def load_data( self: Self ) -> bool:
    #     try:
    #         with open( self.filepath, "b" ) as reader:
    #             dataobj: BoolColumn = pkl.load(reader)
    #
    #             self.refcnt      = dataobj.refcnt
    #             self.keyvaluecnt = dataobj.keyvaluecnt
    #             self.pos_set     = dataobj.pos_set
    #             self.neg_set     = dataobj.neg_set
    #
    #         return True
    #
    #     except Exception as exc:
    #         print(
    #             f"BoolColumn[{self.id}].load_data() - root_dir: {self.filepath} Exception: {exc}"
    #         )
    #         return False

