
from abc import abstractmethod
from typing import Self, Protocol
from sortedcontainers import SortedList

from .. import KValueDict, KeyDefInterface

class GNodeInterface( Protocol ):
    id: str

class NodeDict[ TNode: GNodeInterface ]( GNodeInterface, dict[ str, GNodeInterface ] ):

    def __init__(self: Self, id: str) -> None:
        super(NodeDict, self).__init__()
        self.id = id

    def add( self: Self, item: TNode ) -> None:
        self[ item.id ] = item

    def __add__( self: Self, other: TNode ) -> None:
        self[ other.id ] = other

    @abstractmethod
    def __missing__(self: Self, key: str) -> TNode:
        new_node: GNodeInterface = GNodeInterface.__new__( GNodeInterface )
        self[key] = new_node
        return new_node

class IndexedNodeList[ TNode: GNodeInterface ]( GNodeInterface, SortedList[ GNodeInterface ] ):
    def __init__( self: Self, id: str ) -> None:
        super(IndexedNodeList, self).__init__()
        self.id = id

class RecordBase:

    def __init__( self: Self, rec_index: int ) -> None:
        self.rec_index: int = rec_index
        self.values: KValueDict | None = None

class GraphRecordRoot( Protocol ):

    def graph_id(self: Self) -> str:
        pass

    def add_record( self: Self, graph_rec: RecordBase ) -> None:
        pass

    def apply_logvalue( self: Self, graph_rec: RecordBase, _log_key: str, value: str ) -> None:
        pass

    def __getitem__(self, key: str) -> KeyDefInterface:
        pass





