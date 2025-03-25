from __future__ import annotations

from abc import abstractmethod
from collections import defaultdict

from typing import Self, TypeVar, Any


"""--------------------------------------------------------------
    NodeBase is the root of the hierarchy  
"""
class NodeBase:

    def __init__(self: Self, id:str, **kwargs):
        self.id: str = id

    def __str__(self: Self) -> str:
        return f'{self.__class__.__name__}: {self.id}'

    def __repr__(self: Self) -> str:
        return self.__str__()

TNODE = TypeVar( 'TNODE', bound = NodeBase )

"""--------------------------------------------------------------
    TNode is a genericing layer to keep the fileparse node clean of generics 
"""
class TNode[ T: NodeBase ]( NodeBase ):

    def __init__(self: Self, id: str, **kwargs: dict[str, Any]):
        self.kwargs = kwargs
        super(TNode, self).__init__(id=id)

    @classmethod
    def newnode( cls, id: str = '', **kwargs ) -> NodeBase:
        return cls(id=id, kwargs=kwargs)

class NodeDict[TNODE]( NodeBase, defaultdict[ str, TNODE ] ):

    def __init__(self: Self, id: str):
        super(NodeDict, self).__init__(id=id)

    def add( self: Self, item: TNODE ) -> None:
        self[ item.id ] = item

    def __add__(self: Self, other: TNODE) -> None:
        self[ other.id ] = other

    @abstractmethod
    def __missing__(self, key) -> TNODE:
        pass

class IndexedNodeList[TNODE]( NodeBase, list[TNODE ] ):
    #id: str = Field( None, alias="id" )
    # list: defaultdict[int,T] = []
    def __init__(self: Self, id:str):
        super(IndexedNodeList, self).__init__(id=id)

    #def add_item(self: Self, item: T) -> None:
    #    self[len(self.list)] = item

    #def __add__(self: Self, other: T):
    #    self[len(self.list)] = other


