from typing import Self

import os

from src.gengraphlib.common import (
    KeyType,
    KeyValTypes,
    KeyDefInterface,
    ColumnInterface
)

#from .. import GNodeInterface

class Column[ T: KeyValTypes ]( ColumnInterface ):
    def __init__(self: Self, _key_def: KeyDefInterface, index_dir: str) -> None:
        super( Column, self ).__init__()
        self.key_def:   KeyDefInterface = _key_def
        self.id:        str             = _key_def.key
        self.index_dir: str             = index_dir
        self.keytype:   KeyType | None  = None
        self.unique:    bool            = True

    def init_index( self ) -> bool:
        try:
            os.mkdir( self.index_dir )
            return True

        except Exception as exc:
            print(f"KeyValues[{self.id}] root_dir: {self.index_dir} Exception: {exc}")
            return False

    def __repr__(self: Self) -> str:
        return f'{{ key: "{self.key}", alias: "{self.alias}", unique:{self.unique} }}'



