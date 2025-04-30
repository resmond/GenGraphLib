from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Self

import os
import pickle as pkl
import pyarrow as par

from ..common import (
    KeyValTypes,
    ColumnInterface,
    KeyInfo,
    LineRefList
)

class Column[ T: KeyValTypes ]( ColumnInterface, ABC ):
    def __init__( self: Self, keyinfo: KeyInfo, datadir: str, load_file: bool = False ) -> None:
        super().__init__()
        self.keyinfo:  KeyInfo = keyinfo
        self.id:       str     = self.keyinfo.key
        self.filepath: str     = os.path.join( datadir, f'{self.keyinfo.key}.column')

        if load_file:
            self.read_file()

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
        return self.key, self.partype

    @abstractmethod
    def get_arrowdata( self: Self ) -> tuple[ par.DataType, list[ T | None ], bool ] | None: ...

    def read_file( self: Self ) -> bool:
        try:
            if os.path.exists(self.filepath):
                with open( file=self.filepath, mode="rb" ) as reader:
                    dataobj: Column = pkl.load(reader)
                    self.apply_objdata( dataobj )
                return True
            else:
                return False
        except Exception as exc:
            print(f"Column[{self.keytype}-{self.id}].read_file( {self.filepath} ) Exception: {exc}")
            return False

    def write_file( self: Self ) -> bool:
        try:
            with open( self.filepath, "wb" ) as writer:
                buffer: bytes = pkl.dumps( self )
                writer.write(buffer)


            return True
        except Exception as exc:
            f"Column[{self.keytype}-{self.id}].write_file( {self.filepath} ) Exception: {exc}"
            return False





