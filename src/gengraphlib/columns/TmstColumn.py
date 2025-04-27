from typing import Self

import os
import pickle as pkl

import datetime as dt

from sortedcontainers import SortedDict

from ..common import KeyInfo, LineRefList

from .Column import Column

class TmstColumn( Column[dt.datetime ] ):
    zeroday: dt.datetime = dt.datetime.fromisoformat( "1970-01-01" )

    def __init__( self: Self, keyinfo: KeyInfo, root_dir: str ) -> None:
        super( TmstColumn, self ).__init__( keyinfo, root_dir )

        self.refcnt:         int = -1
        self.keyvaluecnt:    int = -1
        self.keyvaluemap_to_refs: SortedDict[dt.datetime, LineRefList] = SortedDict[dt.datetime, LineRefList]()
        self.valueindex_to_keyvalue: list[ dt.datetime ] = []
        self.ref_to_valueindex:      list[ int ]         = []

    def apply_data( self: Self, keymap: SortedDict[dt.datetime, LineRefList], refcnt: int, skip_write: bool = False ) -> bool:
        try:
            self.keyvaluemap_to_refs = keymap
            self.refcnt = refcnt
            self.keyvaluecnt = len( self.keyvaluemap_to_refs )

            if self.refcnt == 0:
                for key, reflist in self.keyvaluemap_to_refs.items():
                    self.refcnt +=  len(reflist)



            self.valueindex_to_keyvalue = [ TmstColumn.zeroday ] * self.keyvaluecnt
            self.ref_to_valueindex  = [ -1 ] * self.refcnt

            cnt: int = 0
            for key, reflist in self.keyvaluemap_to_refs.items():
                self.valueindex_to_keyvalue[ cnt ] = key
                for ref in reflist:
                    self.ref_to_valueindex[ ref ] = cnt
                cnt += 1

            if not skip_write:
                self.save_data()

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

    def save_data( self: Self ) -> bool:
        try:
            if not os.path.exists(self.batch_dir):
                os.mkdir( self.batch_dir )

            with open( self.filepath, "wb" ) as writer:
                buffer: bytes = pkl.dumps( self )
                writer.write(buffer)

            return True

        except Exception as exc:
            print(f"TmstColumn[{self.id}] root_dir: {self.index_dir} Exception: {exc}")
            return False

    def load_data( self: Self ) -> bool:

        try:
            with open( self.filepath, "b" ) as reader:

                dataobj: TmstColumn = pkl.load( reader )

                self.refcnt                  = dataobj.refcnt
                self.keyvaluecnt             = dataobj.keyvaluecnt
                self.keyvaluemap_to_refs     = dataobj.keyvaluemap_to_refs
                self.valueindex_to_keyvalue  = dataobj.valueindex_to_keyvalue
                self.ref_to_valueindex       = dataobj.ref_to_valueindex

            return True

        except Exception as exc:
            print(f"TmstColumn[{self.id}].load_data() - root_dir: {self.filepath} Exception: {exc}")
            return False


