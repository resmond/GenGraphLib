from collections.abc import Iterable
from typing import Self

from abc import ABC

class GraphSliceItem:

    def __init__( self: Self, *args, **kargs: dict ) -> None:
        super().__init__( *args, **kargs )
        self.id: str = args[0]
        self.alias: str | None = None
        self.len: int | None = None
        
        match len(args):
            case 2 if type(args[1]) is str:
                self.alias: str = args[1]
            case 2 if type(args[1]) is int:
                self.len: int = args[1]
            case 3:
                self.alias: str = args[1]
                self.len: int = args[2]




class GraphSliceDef(list[GraphSliceItem], ABC):

    def __init__(self, names: Iterable[tuple] ):
        if names is not None:
            for name in names:
                self.append(GraphSliceItem(name))
        super().__init__()
        #self.key_group: KeyGroup = key_group


