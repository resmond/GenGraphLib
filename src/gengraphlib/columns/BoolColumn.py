from typing import Self, cast

import os
import pickle as pkl

from sortedcontainers import SortedSet

from ..common import KeyInfo, LineRefList

from .Column import Column

class BoolColumn( Column[bool] ):
    def __init__( self: Self, keyinfo: KeyInfo, root_dir: str ) -> None:
        super( BoolColumn, self ).__init__( keyinfo, root_dir )

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
                self.save_data()

            return True

        except Exception as exc:
            print(f"BoolColumn[{self.id}].apply_data() - Exception: {exc}")
            return False

    def keyvalue_from_recno( self: Self, recno: int ) -> bool | None:
        return recno in self.pos_set

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

    def save_data( self: Self ) -> bool:
        try:
            if not os.path.exists(self.batch_dir):
                os.mkdir( self.batch_dir )

            with open( self.filepath, "wb" ) as writer:
                buffer: bytes = pkl.dumps( self )
                writer.write(buffer)

            return True

        except Exception as exc:
            print(f"BoolColumn[{self.id}] root_dir: {self.index_dir} Exception: {exc}")
            return False

    def load_data( self: Self ) -> bool:
        try:
            with open( self.filepath, "b" ) as reader:
                dataobj: BoolColumn = pkl.load(reader)

                self.refcnt      = dataobj.refcnt
                self.keyvaluecnt = dataobj.keyvaluecnt
                self.pos_set     = dataobj.pos_set
                self.neg_set     = dataobj.neg_set

            return True

        except Exception as exc:
            print(
                f"BoolColumn[{self.id}].load_data() - root_dir: {self.filepath} Exception: {exc}"
            )
            return False

