from abc import ABC, abstractmethod
from typing import Self

import os

from ..common import (
    KeyValTypes,
    ColumnInterface,
    KeyInfo,
    LineRefList,
)

#from .. import GNodeInterface

class Column[ T: KeyValTypes ]( ColumnInterface, ABC ):
    def __init__(self: Self, keyinfo: KeyInfo, root_dir: str ) -> None:
        super().__init__()
        self.keyinfo:   KeyInfo = keyinfo
        self.root_dir:  str     = root_dir
        self.id:        str     = self.keyinfo.key
        self.batch_dir: str     = os.path.join(self.root_dir, self.keyinfo.batch_id, f"{self.keyinfo.key}" )
        self.filepath:  str     = os.path.join(self.root_dir, "boots", self.keyinfo.batch_id,  f"{self.keyinfo.key}-index.bin" )

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
    def save_data( self: Self ) -> bool: ...

    @abstractmethod
    def load_data( self: Self ) -> bool: ...



