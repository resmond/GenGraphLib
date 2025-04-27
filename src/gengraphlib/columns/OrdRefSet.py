from typing import Self

from sortedcontainers import SortedDict
import pickle as pkl

from ..common import LineRefList, KeyValTypes, KeyInfo
from .Column import Column

class KeyValRecIndex[T: KeyValTypes]:

    def __init__( self: Self, keymap: SortedDict[T, LineRefList ], keyinfo: KeyInfo, column: Column[T ], refcnt: int | None = None ) -> None:
        self.column: Column[T] = column
        self.keyinfo:   KeyInfo      = keyinfo
        self.refcnt:    int          = refcnt | keyinfo.refcnt
        self.keymap: SortedDict[T, LineRefList ] = keymap
        self.keycnt:    int          = len( self.keymap )
        self.key_array: list[T]      = []
        self.ref_array: list[int]    = []

    def create_index( self: Self ) -> bool:
        try:
            if self.refcnt == 0:
                for key, reflist in self.keymap.items():
                    self.refcnt +=  len(reflist)

            self.key_array = [] * self.keycnt
            self.ref_array = [] * self.refcnt

            cnt: int = 0
            for key, reflist in self.keymap.items():
                self.key_array[ cnt ] = key
                for ref in reflist:
                    self.ref_array[ ref ] = cnt

            return True

        except Exception as exc:
            print( f"OrdRefSet[{type(T)}.create_keyar()]: Len: {self.reclist_len} Exception: {exc}" )
            return False



