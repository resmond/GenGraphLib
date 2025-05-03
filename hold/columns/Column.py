from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Self

import os
import sys
import pickle as pkl
import pyarrow as par

from src.gengraphlib.common import (
    KeyValTypes,
    ColumnInterface,
    KeyInfo,
    LineRefList
)

class Column[ T: KeyValTypes ]( ColumnInterface, ABC ):
    def __init__( self: Self, keyinfo: KeyInfo, partype: par.DataType, indexdir: str, load_file: bool = False ) -> None:
        super().__init__()
        self.keyinfo:   KeyInfo      = keyinfo
        self.partype:   par.DataType = partype
        self.id:        str          = self.keyinfo.key
        self.index_dir: str          = indexdir
        self.load_file: bool = load_file
        self.filepath:  str  = os.path.join( indexdir, f'{self.keyinfo.key}.column' )

        # if load_file:
        #     self.load_fromfile()

    @abstractmethod
    def keyvalue_from_recno( self: Self, recno: int ) -> T | None: ...

    @abstractmethod
    def keyvalue_from_valueindex( self: Self, valueindex: int ) -> T | None: ...

    @abstractmethod
    def valueindex_from_recno( self: Self, recno: int ) -> int | None: ...

    @abstractmethod
    def valueindex_from_keyvalue( self: Self, keyvalue: T ) -> int | None: ...

    @abstractmethod
    def refs_from_keyvalue( self: Self, keyvalue: T ) -> LineRefList | None: ...

    @abstractmethod
    def refs_from_valueindex( self: Self, valueindex: int ) -> LineRefList | None: ...

    @abstractmethod
    def apply_objdata( self: Self, objdata: Self ) -> bool: ...

    def get_arrowfield( self: Self ) -> tuple[str, par.DataType]:
        return self.id, self.partype

    @abstractmethod
    def get_arrowdata( self: Self ) -> tuple[ par.DataType, list[ T | None ], bool ] | None: ...

    @abstractmethod
    def get_pararray( self: Self ) -> par.Array | None: ...

    def load_fromfile( self: Self ) -> bool:
        try:
            if os.path.exists(self.filepath):
                sys.path.append( "/src" )
                with open( file=self.filepath, mode="rb" ) as reader:
                    dataobj: Column = pkl.load(reader)
                    self.apply_objdata( dataobj )
                return True
            else:
                return False
        except Exception as exc:
            print(f"Column[{self.keytype}-{self.id}].read_file( {self.filepath} ) Exception: {exc}")
            return False

    def write_tofile( self: Self ) -> bool:
        try:
            with open( self.filepath, "wb" ) as writer:
                buffer: bytes = pkl.dumps( self )
                writer.write(buffer)

            return True
        except Exception as exc:
            f"Column[{self.keytype}-{self.id}].write_file( {self.filepath} ) Exception: {exc}"
            return False





