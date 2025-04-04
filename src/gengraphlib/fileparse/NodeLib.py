from abc import abstractmethod
from typing import Self, TypeVar
from sortedcontainers import SortedList



"""--------------------------------------------------------------
    NodeBase is the root of the hierarchy  
"""
class NodeBase:

    def __init__(self: Self, id:str):
        self.id: str = id

    def __str__(self: Self) -> str:
        return f'{self.__class__.__name__}: {self.id}'

    def __repr__(self: Self) -> str:
        return self.__str__()

#    @classmethod
#    def newnode( cls, id: str = '', **kwargs ) -> NodeBase:
#        return cls(id=id, kwargs=kwargs)


TNode = TypeVar( 'TNode', bound = NodeBase )

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

class NodeDict[Tnode: NodeBase]( NodeBase, dict[ str, Tnode ] ):

    def __init__(self: Self, id: str):
        super(NodeDict, self).__init__(id=id)

    def add( self: Self, item: TNode ) -> None:
        self[ item.id ] = item

    def __add__( self: Self, other: TNode ) -> None:
        self[ other.id ] = other

    @abstractmethod
    def __missing__(self, key: str) -> TNode:
        new_node: TNode = TNode.__new__(TNode)
        self[key] = new_node
        return new_node


class IndexedNodeList[ TNode: NodeBase ]( NodeBase, SortedList[TNode] ):
    #id: str = Field( None, alias="id" )
    # list: defaultdict[int,T] = []
    def __init__(self: Self, id:str):
        super(IndexedNodeList, self).__init__(id=id)

    #def add_item(self: Self, item: T) -> None:
    #    self[len(self.list)] = item

    #def __add__(self: Self, other: T):
    #    self[len(self.list)] = other


