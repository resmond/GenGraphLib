from typing import Self

from sortedcontainers import SortedDict

from ..common import KeyInfo, LineRefList

from . import Column

class StrColumn( Column[str] ):
    def __init__( self: Self, keyinfo: KeyInfo, datadir: str, load_data: bool = False ) -> None:
        super( StrColumn, self ).__init__( keyinfo, datadir, load_data )

        self.refcnt:         int = -1
        self.maxrecnum:      int = -1
        self.keyvaluecnt:    int = -1
        self.keyvaluemap_to_refs: SortedDict[ str, LineRefList ] = SortedDict[str, LineRefList ]()
        self.valueindex_to_keyvalue: list[ str ] = []
        self.ref_to_valueindex:      list[ int ] = []

        if load_data:
            self.read_file()

    def apply_data( self: Self, keymap: SortedDict[str, LineRefList], refcnt: int, maxrecnum: int, skip_write: bool = False ) -> bool:
        try:
            self.keyvaluemap_to_refs = keymap
            self.refcnt = refcnt
            self.maxrecnum = maxrecnum
            self.keyvaluecnt = len( self.keyvaluemap_to_refs )

            if self.refcnt == 0:
                for key, reflist in self.keyvaluemap_to_refs.items():
                    self.refcnt +=  len(reflist)

            self.valueindex_to_keyvalue = [ "" ] * self.keyvaluecnt
            self.ref_to_valueindex  = [ -1 ] * self.maxrecnum

            valueindex: int = 0
            for key, reflist in self.keyvaluemap_to_refs.items():
                self.valueindex_to_keyvalue[ valueindex ] = key
                for ref in reflist:
                    self.ref_to_valueindex[ ref ] = valueindex
                valueindex += 1

            if not skip_write:
                self.write_file()

            return True

        except Exception as exc:
            print(f"StrColumn[{self.id}].apply_data() - Exception: {exc}")
            return False

    def keyvalue_from_recno( self: Self, recno: int ) -> str | None:
        if recno < self.refcnt:
            valueindex:   int  = self.ref_to_valueindex[ recno ]
            rec_keyvalue: str = self.valueindex_to_keyvalue[ valueindex ]
            return rec_keyvalue
        else:
            return None

    def keyvalue_from_valueindex( self: Self, valueindex: int ) -> str | None:
        if valueindex < len(self.valueindex_to_keyvalue):
            value = self.valueindex_to_keyvalue[ valueindex ]
            return value
        else:
            return None

    def valueindex_from_recno( self: Self, recno: int ) -> int | None:
        if recno < self.refcnt:
            valindex: int  = self.ref_to_valueindex[ recno ]
            return valindex
        else:
            return None

    def valueindex_from_keyvalue( self: Self, keyvalue: str ) -> int | None:
        if keyvalue in self.keyvaluemap_to_refs:
            ref_list: LineRefList = self.keyvaluemap_to_refs[ keyvalue ]
            first_rec: int = ref_list[0]
            return self.ref_to_valueindex[ first_rec ]
        else:
            return None

    def refs_from_keyvalue( self: Self, keyvalue: str ) -> LineRefList | None:
        if keyvalue in self.keyvaluemap_to_refs:
            return self.keyvaluemap_to_refs[ keyvalue ]
        else:
            return None

    def refs_from_valueindex( self: Self, valueindex: int ) -> LineRefList | None:
        if valueindex < len(self.valueindex_to_keyvalue):
            key: str = self.valueindex_to_keyvalue[ valueindex ]
            return self.keyvaluemap_to_refs[ key ]
        else:
            return None

    def apply_load( self: Self, dataobj: Self ) -> bool:

        self.refcnt                 = dataobj.refcnt
        self.keyvaluecnt            = dataobj.keyvaluecnt
        self.keyvaluemap_to_refs    = dataobj.keyvaluemap_to_refs
        self.valueindex_to_keyvalue = dataobj.valueindex_to_keyvalue
        self.ref_to_valueindex      = dataobj.ref_to_valueindex

        return True
