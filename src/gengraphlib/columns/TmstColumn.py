from typing import Self

import datetime as dt

from sortedcontainers import SortedDict

from ..common import KeyInfo, LineRefList

from .Column import Column

class TmstColumn( Column[dt.datetime ] ):
    zeroday: dt.datetime = dt.datetime.fromisoformat( "1970-01-01" )

    def __init__( self: Self, keyinfo: KeyInfo, datadir: str, load_data: bool = False ) -> None:
        super( TmstColumn, self ).__init__( keyinfo, datadir, load_data )

        self.refcnt:         int = -1
        self.maxrecnum:      int = -1
        self.keyvaluecnt:    int = -1
        self.keyvaluemap_to_refs: SortedDict[ dt.datetime, LineRefList ] = SortedDict[dt.datetime, LineRefList]()
        self.valueindex_to_keyvalue: list[ dt.datetime ] = []
        self.ref_to_valueindex:      list[ int ]         = []

    def apply_data( self: Self, keymap: SortedDict[dt.datetime, LineRefList ], refcnt: int, maxrecnum: int, skip_write: bool = False ) -> bool:
        try:
            self.keyvaluemap_to_refs = keymap
            self.refcnt = refcnt
            self.maxrecnum = maxrecnum
            self.keyvaluecnt = len( self.keyvaluemap_to_refs )

            if self.refcnt == 0:
                for key, reflist in self.keyvaluemap_to_refs.items():
                    self.refcnt +=  len(reflist)

            self.valueindex_to_keyvalue = [ TmstColumn.zeroday ] * self.keyvaluecnt
            self.ref_to_valueindex  = [ -1 ] * self.maxrecnum

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
            print(f"StrColumn[{self.id}].apply_data() - Exception: {exc}")
            return False

    def keyvalue_from_recno( self: Self, recno: int ) -> dt.datetime | None:
        if recno < self.refcnt:
            valueindex:   int  = self.ref_to_valueindex[ recno ]
            rec_keyvalue: dt.datetime = self.valueindex_to_keyvalue[ valueindex ]
            return rec_keyvalue
        else:
            return None

    def keyvalue_from_valueindex( self: Self, valueindex: int ) -> dt.datetime | None:
        if valueindex < len(self.valueindex_to_keyvalue):
            keyvalue: dt.datetime = self.valueindex_to_keyvalue[ valueindex ]
            return keyvalue
        else:
            return None

    def valueindex_from_recno( self: Self, recno: int ) -> int | None:
        if recno < self.refcnt:
            valindex: int  = self.ref_to_valueindex[ recno ]
            return valindex
        else:
            return None

    def valueindex_from_keyvalue( self: Self, keyvalue: dt.datetime ) -> int | None:
        if keyvalue in self.keyvaluemap_to_refs:
            ref_list: LineRefList = self.keyvaluemap_to_refs[ keyvalue ]
            first_rec: int = ref_list[0]
            return self.ref_to_valueindex[ first_rec ]
        else:
            return None

    def refs_from_keyvalue( self: Self, keyvalue: dt.datetime ) -> LineRefList | None:
        if keyvalue in self.keyvaluemap_to_refs:
            return self.keyvaluemap_to_refs[ keyvalue ]
        else:
            return None

    def refs_from_valueindex( self: Self, valueindex: int ) -> LineRefList | None:
        if valueindex < len(self.valueindex_to_keyvalue):
            keyvalue: dt.datetime = self.valueindex_to_keyvalue[ valueindex ]
            return self.keyvaluemap_to_refs[ keyvalue ]
        else:
            return None

    def apply_objdata( self: Self, objdata: Self ) -> bool:

        self.refcnt                 = objdata.refcnt
        self.keyvaluecnt            = objdata.keyvaluecnt
        self.keyvaluemap_to_refs    = objdata.keyvaluemap_to_refs
        self.valueindex_to_keyvalue = objdata.valueindex_to_keyvalue
        self.ref_to_valueindex      = objdata.ref_to_valueindex

        return True

    def get_arrowdata( self: Self ) -> tuple[list[dt.datetime ], bool ]:
        col_array = list[dt.datetime]()
        for row in self.ref_to_valueindex:
            col_array.append( self.valueindex_to_keyvalue[ row ] )
        return col_array, False
