from __future__ import annotations

from collections.abc import Set, Iterable
from typing import Self, Protocol

from .GraphNodeLib import GraphNodeBase
from .. import KeyValues

class KeyGraphRoot(Protocol):

    @property
    def graph_id(self: Self) -> str:
        pass

    def add_graphrec( self: Self, graph_rec: GraphRecordBase ) -> None:
        pass

class GraphRec( Set[KeyValues] ):

    def __init__( self: Self, graph_root: KeyGraphRoot, rec_index: int ) -> None:
        pass

    def __contains__( self, x : KeyValues ) -> bool:
        pass

    def __len__( self ) -> int:
        pass

    def __iter__( self ) -> Iterable[KeyValues ]:
        pass

class GraphRecordBase( GraphNodeBase ):

    def __init__( self: Self, _graph: KeyGraphRoot , rec_index: int, line_str: str | None = None ) -> None:
        super().__init__( str( rec_index ) )
        self.line_str: str = line_str
        self.line_num: int = rec_index

