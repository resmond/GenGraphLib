from abc import ABC, abstractmethod
from typing import Self, Union

import datetime as dt

from sortedcontainers import SortedDict

from src.gengraphlib import KeyValTypes, KeyDefBase


class LineRefList( list[ int ] ):
    pass

class KeyValueTriggerBase[ T: KeyValTypes ]( ABC ):

    def __init__( self ):
        super().__init__()

    @abstractmethod
    def eval( self, value: T ) -> Self:
        pass

AddValueResult: type = Union[ KeyValueTriggerBase | None ]

class ValueResults( dict[str, KeyValTypes] ):

    def __init__( self: Self, _json_key: str, _value: KeyValTypes ):
        super().__init__()
        self.json_key: str = _json_key
        self.value: KeyValTypes = _value

class KeyValues[ T: KeyValTypes ]( SortedDict[ T, LineRefList ] ):

    def __init__( self: Self, _key_def: KeyDefBase[T] ) -> None:
        self.key_def = _key_def
        self.unique: bool = True
        super().__init__()
        self.triggers: list[ KeyValueTriggerBase[T] ] | None = None

    def add_trigger( self: Self, trigger: KeyValueTriggerBase[T] ) ->  None:
        if self.triggers is None:
            self.triggers = list[ KeyValueTriggerBase[T] ]()

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

    def get_valuestr( self: Self ) -> str:
        pass

class StrKeyValueSet( KeyValues[str] ):
    def __init__( self: Self, _key_def: KeyDefBase[str] ) -> None:
        super().__init__( _key_def )

class IntKeyValueSet( KeyValues[int ] ):
    def __init__( self: Self, _key_def: KeyDefBase[int] ) -> None:
        super().__init__( _key_def )

class BoolKeyValueSet( KeyValues[bool] ):
    def __init__( self: Self, _key_def: KeyDefBase[bool] ) -> None:
        super().__init__( _key_def )

class FloatKeyValueSet( KeyValues[float] ):
    def __init__( self: Self, _key_def: KeyDefBase[float] ) -> None:
        super().__init__( _key_def )

class TmstKeyValueSet( KeyValues[dt.datetime ] ):
    def __init__( self: Self, _key_def: KeyDefBase[dt.datetime] ) -> None:
        super().__init__( _key_def )




