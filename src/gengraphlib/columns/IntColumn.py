from typing import Self

import pyarrow as par

from sortedcontainers import SortedDict

from ..common import LineRefList, KeyInfo

from .Column import Column

class IntColumn( Column[int] ):
    def __init__( self: Self, keyinfo: KeyInfo, datadir: str, load_data: bool = False ) -> None:
        super( IntColumn, self ).__init__( keyinfo, datadir, load_data )

        self.refcnt:         int = -1
        self.maxrecnum:      int = -1
        self.keyvaluecnt:    int = -1
        self.keyvaluemap_to_refs: SortedDict[ int, LineRefList ] = SortedDict[int, LineRefList ]()
        self.valueindex_to_keyvalue: list[ int ] = []
        self.ref_to_valueindex:      list[ int ] = []

    def apply_data( self: Self, keymap: SortedDict[int, LineRefList ], refcnt: int, maxrecnum: int, skip_write: bool = False ) -> bool:
        try:
            self.keyvaluemap_to_refs = keymap
            self.refcnt = refcnt
            self.maxrecnum = maxrecnum
            self.keyvaluecnt = len( self.keyvaluemap_to_refs )

            if self.refcnt == 0:
                for key, reflist in self.keyvaluemap_to_refs.items():
                    self.refcnt +=  len(reflist)

            self.valueindex_to_keyvalue = [ -1 ] * self.keyvaluecnt
            self.ref_to_valueindex = [ -1 ] * self.maxrecnum

            cnt: int = 0
            for key, reflist in self.keyvaluemap_to_refs.items():
                self.valueindex_to_keyvalue[ cnt ] = key
                for ref in reflist:
                    self.ref_to_valueindex[ ref ] = cnt
                cnt += 1

            if not skip_write:
                self.write_file()

            return True

        except Exception as exc:
            print(f"IntColumn[{self.id}].apply_data() - Exception: {exc}")
            return False

    def keyvalue_from_recno( self: Self, recno: int ) -> int | None:
        if recno <= self.refcnt:
            valueindex: int  = self.ref_to_valueindex[ recno ]
            keyvalue: int = self.valueindex_to_keyvalue[ valueindex ]
            return keyvalue
        else:
            return None

    def keyvalue_from_valueindex( self: Self, valueindex: int ) -> int | None:
        if valueindex < len( self.valueindex_to_keyvalue ):
            keyvalue: int = self.valueindex_to_keyvalue[ valueindex ]
            return keyvalue
        else:
            return None

    def valueindex_from_recno( self: Self, recno: int ) -> int | None:
        if recno <= self.refcnt:
            valindex: int  = self.ref_to_valueindex[ recno ]
            return valindex
        else:
            return None

    def valueindex_from_keyvalue( self: Self, keyvalue: int ) -> int | None:
        if keyvalue in self.keyvaluemap_to_refs:
            ref_list: LineRefList = self.keyvaluemap_to_refs[ keyvalue ]
            first_rec: int = ref_list[0]
            return self.ref_to_valueindex[ first_rec ]
        else:
            return None

    def refs_from_keyvalue( self: Self, keyvalue: int ) -> LineRefList | None:
        if keyvalue in self.keyvaluemap_to_refs:
            return self.keyvaluemap_to_refs[ keyvalue ]
        else:
            return None

    def refs_from_valueindex( self: Self, valueindex: int ) -> LineRefList | None:
        if valueindex < len( self.valueindex_to_keyvalue ):
            key: int = self.valueindex_to_keyvalue[ valueindex ]
            return self.keyvaluemap_to_refs[ key ]
        else:
            return None

    def apply_objdata( self: Self, objdata: Self ) -> bool:

        self.refcnt                 = objdata.refcnt
        self.keyvaluecnt            = objdata.keyvaluecnt
        self.keyvaluemap_to_refs    = objdata.keyvaluemap_to_refs
        self.valueindex_to_keyvalue = objdata.valueindex_to_keyvalue
        self.ref_to_valueindex      = objdata.ref_to_valueindex

        return True

    def get_arrowdata( self: Self ) -> tuple[ par.DataType, list[int|None ], bool ] | None:

        max_valueindex = len(self.valueindex_to_keyvalue)
        if max_valueindex > 0:
            col_array = list[int|None]()
            for valueindex in self.ref_to_valueindex:
                if valueindex < max_valueindex:
                    col_array.append( self.valueindex_to_keyvalue[valueindex] )
                else:
                    col_array.append( None )

            return par.int64(), col_array, False
        else:
            return None



