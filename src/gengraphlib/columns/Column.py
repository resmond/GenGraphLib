from abc import ABC, abstractmethod
from typing import Self

from ..common import (
    KeyValTypes,
    ColumnInterface,
    KeyInfo,
    LineRefList,
)

from .GraphTable import GraphTable

#from .. import GNodeInterface

class Column[ T: KeyValTypes ]( ColumnInterface, ABC ):
    def __init__(self: Self, keyinfo: KeyInfo, graph_table: GraphTable ) -> None:
        super().__init__()
        self.keyinfo:     KeyInfo    = keyinfo
        self.graph_table: GraphTable = graph_table
        self.id:          str        = self.keyinfo.key
        #self.batch_dir: str     = os.path.join(self.root_dir, "boots", self.keyinfo.batch_id )
        #self.filepath:  str     = os.path.join(self.batch_dir,  f"{self.keyinfo.key}-index.bin" )
        #print(self.filepath)


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



