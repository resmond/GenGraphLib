from abc import abstractmethod
from typing import Self, TypeVar
from sortedcontainers import SortedList

"""
    NodeBase is the root of the hierarchy
      
"""
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


