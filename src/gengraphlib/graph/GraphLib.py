from abc import abstractmethod
from asyncio import Protocol
from typing import Self, TypeVar
from sortedcontainers import SortedList, SortedDict

from src.gengraphlib import KeyType, KeyValTypes

class LineRefList( list[ int ] ):
    pass

class GraphNodeBase:

    def __init__(self: Self, id: str) -> None:
        self.id: str = id
        super(GraphNodeBase, self).__init__()

TGraphNode = TypeVar( 'TGraphNode', bound = GraphNodeBase )

class NodeDict[ TNode: GraphNodeBase ]( GraphNodeBase, dict[ str, TNode ] ):

    def __init__(self: Self, id: str) -> None:
        super(NodeDict, self).__init__(id=id)

    def add( self: Self, item: TNode ) -> None:
        self[ item.id ] = item

    def __add__( self: Self, other: TNode ) -> None:
        self[ other.id ] = other

    @abstractmethod
    def __missing__(self: Self, key: str) -> TNode:
        new_node: TGraphNode = TGraphNode.__new__( TGraphNode )
        self[key] = new_node
        return new_node

class IndexedNodeList[ TNode: GraphNodeBase ]( GraphNodeBase, SortedList[TNode ] ):
    def __init__( self: Self, id: str ) -> None:
        super(IndexedNodeList, self).__init__(id=id)

class RecordBase( GraphNodeBase ):

    def __init__( self: Self, rec_index: int, line_str: str | None = None ) -> None:
        super(RecordBase, self).__init__( str( rec_index ) )
        self.rec_str: str = line_str
        self.rec_index: int = rec_index

class GraphRecordRoot( Protocol ):

    def graph_id(self: Self) -> str:
        pass

    def add_record( self: Self, graph_rec: RecordBase ) -> None:
        pass

class KeyDefSig[T: KeyValTypes](Protocol):
    json_key: str
    log_key: str
    key_type: KeyType
    groups: list[str] | None

class KeyDefBase[T: KeyValTypes ]( KeyDefSig ):
    def __init__( self: Self, _json_key: str, _log_key: str, _key_type: KeyType, groups: list[str] | str | None = None) -> None:
        super(KeyDefBase, self).__init__()
        self.json_key: str = _json_key
        self.log_key: str = _log_key
        self.key_type: KeyType = _key_type
        self.groups: list[str] | None = None
        self._skip: bool = True
        self._event_trigger: bool = False
        self.key_values: KeyValues[T] = KeyValues[T]( self )

        match groups:
            case str() if groups in ["skip", ""]:
                pass
            case str():
                self.groups = [groups]
                self._skip = False
            case [] if len(groups) > 0:
                self.groups = groups
                self._skip = False

    @property
    def dologing( self: Self ) -> bool:
        return not self._skip

class KeyDefDict( dict[str, KeyDefBase ] ):
    pass

class KeyValues[ T: KeyValTypes ]( SortedDict[ T, LineRefList ] ):

    def __init__( self: Self, _key_def: KeyDefSig[T] ) -> None:
        self.key_def: KeyDefSig[T] = _key_def
        self.unique: bool = True
        super(KeyValues, self).__init__()

    def __repr__( self: Self ) -> str:
        return f'{{unique:{self.unique}, cnt:{len(self)}'


