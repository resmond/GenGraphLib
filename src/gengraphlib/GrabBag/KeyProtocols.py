from abc import ABC, abstractmethod
from typing import Self

from collections.abc import Iterable, Mapping, Sequence, AsyncIterator, Callable

from typing_extensions import Protocol

class NodeId(Protocol):

    @property
    def id( self ) -> str:
        pass

class NodeIndex[ TNode: NodeId ]( NodeId, Mapping[ str, TNode ], Sequence[ TNode ], ABC ):

    @abstractmethod
    @property
    def id( self ) -> str:
        pass

    @abstractmethod
    def __getitem__( self: Self, key, / ):
        pass

    @abstractmethod
    def __len__( self: Self ) -> int:
        pass

    @abstractmethod
    def keys(self) -> Iterable[str]:
        pass

    @abstractmethod
    def items(self) -> Iterable[tuple[str,TNode ] ]:
        pass

    @abstractmethod
    def values(self) -> Iterable[ TNode ]:
        pass

    @abstractmethod
    def get(self, key, default=None) -> TNode | None:
        pass

    @abstractmethod
    def __contains__(self, key) -> bool:
        pass

    @abstractmethod
    def traverse(self) -> Iterable[TNode]:
        pass

class AsyncTraverse[ TNode: NodeId ]( AsyncIterator[ TNode ], ABC ):

    @abstractmethod
    def traverse(self) -> Iterable[TNode]:
        pass

    @abstractmethod
    async def async_traverse(self: Self, traverse_fn: Callable[ [ TNode ], bool ] | None) -> AsyncIterator[ TNode ]:
        pass


class GraphNodeBase(NodeId):

    def __init__(self: Self, id: str = None ) -> None:
       self.id = id



class TestNode(GraphNodeBase):

    def __init__(self: Self, id: str = None ) -> None:
        super().__init__(id)





if __name__ == "__main__":
    node = GraphNodeBase()

    print(node.id)

