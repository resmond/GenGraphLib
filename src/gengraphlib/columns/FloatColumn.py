from typing import Self

from sortedcontainers import SortedDict

from ..common import KeyInfo, LineRefList

from .Column import Column

class FloatColumn( Column[float ] ):
    def __init__( self: Self, keyinfo: KeyInfo, datadir: str, load_data: bool = False ) -> None:
        super( FloatColumn, self ).__init__( keyinfo, datadir, load_data )

        self.refcnt:         int = -1
        self.maxrecnum:      int = -1
        self.keyvaluecnt:    int = -1
        self.keyvaluemap_to_refs: SortedDict[float, LineRefList] = SortedDict[float, LineRefList]()
        self.valueindex_to_keyvalue: list[ float ] = []
        self.ref_to_valueindex:      list[ int ] = []

    def apply_data( self: Self, keymap: SortedDict[float, LineRefList], refcnt: int, maxrecnum: int, skip_write: bool = False ) -> bool:
        try:
            self.keyvaluemap_to_refs = keymap
            self.refcnt    = refcnt
            self.maxrecnum = maxrecnum
            self.keyvaluecnt = len( self.keyvaluemap_to_refs )

            if self.refcnt == 0:
                for key, reflist in self.keyvaluemap_to_refs.items():
                    self.refcnt +=  len(reflist)

            self.valueindex_to_keyvalue = [ -0.1 ] * self.keyvaluecnt
            self.ref_to_valueindex      = [  -1  ] * self.maxrecnum

            cnt: int = 0
            for key, reflist in self.keyvaluemap_to_refs.items():
                self.valueindex_to_keyvalue[ cnt ] = key
                for ref in reflist:
                    self.ref_to_valueindex[ ref ] = cnt
                cnt += 1

            if not skip_write:
                self.save()

            return True

        except Exception as exc:
            print(f"FloatColumn[{self.id}].apply_data() - Exception: {exc}")
            return False

    def keyvalue_from_recno( self: Self, recno: int ) -> float | None:
        if recno <= self.refcnt:
            valueindex: int  = self.ref_to_valueindex[ recno ]
            keyvalue: float = self.valueindex_to_keyvalue[ valueindex ]
            return keyvalue
        else:
            return None

    def keyvalue_from_valueindex( self: Self, valueindex: int ) -> float | None:
        if valueindex < len( self.valueindex_to_keyvalue ):
            keyvalue: float = self.valueindex_to_keyvalue[ valueindex ]
            return keyvalue
        else:
            return None

    def valueindex_from_recno( self: Self, recno: int ) -> int | None:
        if recno <= self.refcnt:
            valindex: int  = self.ref_to_valueindex[ recno ]
            return valindex
        else:
            return None

    def valueindex_from_keyvalue( self: Self, keyvalue: float ) -> int | None:
        if keyvalue in self.keyvaluemap_to_refs:
            ref_list: LineRefList = self.keyvaluemap_to_refs[ keyvalue ]
            first_rec: int = ref_list[0]
            return self.ref_to_valueindex[ first_rec ]
        else:
            return None

    def refs_from_keyvalue( self: Self, keyvalue: float ) -> LineRefList | None:
        if keyvalue in self.keyvaluemap_to_refs:
            return self.keyvaluemap_to_refs[ keyvalue ]
        else:
            return None

    def refs_from_valueindex( self: Self, valueindex: int ) -> LineRefList | None:
        if valueindex < len( self.valueindex_to_keyvalue ):
            keyvalue: float = self.valueindex_to_keyvalue[ valueindex ]
            return self.keyvaluemap_to_refs[ keyvalue ]
        else:
            return None

    def apply_load( self: Self, dataobj: Self ) -> bool:

        self.refcnt                 = dataobj.refcnt
        self.keyvaluecnt            = dataobj.keyvaluecnt
        self.keyvaluemap_to_refs    = dataobj.keyvaluemap_to_refs
        self.valueindex_to_keyvalue = dataobj.valueindex_to_keyvalue
        self.ref_to_valueindex      = dataobj.ref_to_valueindex

        return True


