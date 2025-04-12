from abc import abstractmethod
from typing import Self, TypeVar
from sortedcontainers import SortedList

"""
    NodeBase is the root of the hierarchy
      
"""


class GraphNodeBase:

    def __init__(self: Self, id: str):
        super(GraphNodeBase, self).__init__()
        self.id: str = id




TGraphNode = TypeVar( 'TGraphNode', bound = GraphNodeBase )

"""--------------------------------------------------------------
    TNode is a genericing layer to keep the fileparse node clean of generics 
"""
"""
class TNode[ T: NodeBase ]( NodeBase ):

    def __init__(self: Self, id: str, **kwargs: dict[str, Any]):
        self.kwargs = kwargs
        super(TNode, self).__init__(id=id)

    @classmethod
    def newnode( cls, id: str = '', **kwargs ) -> NodeBase:
        return cls(id=id, kwargs=kwargs)
"""

class NodeDict[ TNode: GraphNodeBase ]( GraphNodeBase, dict[ str, TNode ] ):

    def __init__(self: Self, id: str):
        super().__init__(id=id)

    def add( self: Self, item: TGraphNode ) -> None:
        self[ item.id ] = item

    def __add__( self: Self, other: TGraphNode ) -> None:
        self[ other.id ] = other

    @abstractmethod
    def __missing__(self, key: str) -> TGraphNode:
        new_node: TGraphNode = TGraphNode.__new__( TGraphNode )
        self[key] = new_node
        return new_node


class IndexedNodeList[ TNode: GraphNodeBase ]( GraphNodeBase, SortedList[TNode ] ):
    #id: str = Field( None, alias="id" )
    # list: defaultdict[int,T] = []
    def __init__(self: Self, id:str):
        super().__init__(id=id)

    #def add_item(self: Self, item: T) -> None:
    #    self[len(self.list)] = item

    #def __add__(self: Self, other: T):
    #    self[len(self.list)] = other


