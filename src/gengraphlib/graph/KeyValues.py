from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Self, Union

from sortedcontainers import SortedDict

from .. import KeyValTypes

class LineRefList( list[ int ] ):
    pass

class KeyValueTestBase[ T: KeyValTypes ]( ABC ):

    def __init__( self ):
        super(KeyValueTestBase, self).__init__()

    @abstractmethod
    def eval( self, value: T ) -> Self:
        pass

AddValueResult: type = Union[ KeyValueTestBase | None ]

class KeyValueBase[ T: KeyValTypes ]( SortedDict[ T, LineRefList ] ):

    def __init__( self: Self, parent_key: str ) -> None:
        super(KeyValueBase, self).__init__()
        self.triggers: list[KeyValueTestBase[T]] | None = None
        self.parent_key = parent_key
        self.unique: bool = True

    def add_trigger( self: Self, trigger: KeyValueTestBase[T] ) ->  None:
        if self.triggers is None:
            self.triggers = list[KeyValueTestBase[T]]

        self.triggers.append( trigger )

    def add_value( self: Self, new_value: T, line_num: int ) -> AddValueResult:
        if new_value not in self:
            self[new_value] = LineRefList()
            self.unique = False

        self[new_value].append( line_num )

        if self.triggers is not None:
            for trigger in self.triggers:
                if trigger.eval( new_value ):
                    print(f'[KeyValueBase.add_value] Trigger: {new_value}')
                    return trigger

        return None

    def __repr__( self: Self ) -> str:
        return f'{{unique:{self.unique}, cnt:{len(self)}'

