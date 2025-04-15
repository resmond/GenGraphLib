from typing import Self

import datetime as dt

from sortedcontainers import SortedDict

from .. import (
    KeyType,
    KeyValTypes,
    LineRefList,
    value_event_fn
)

from .. import (
    KeyDefInterface,
    KeyValuesInterface,
    KeyValueEvent
)

#from .. import GNodeInterface

class KeyValues[T: KeyValTypes]( SortedDict[T, LineRefList], KeyValuesInterface ):
    def __init__(self: Self, _key_def: KeyDefInterface[T]) -> None:
        super(KeyValues, self).__init__()

        self.key_type: KeyType
        self.value_event_fn: value_event_fn = self.value_event

        self.key_def: KeyDefInterface[T] = _key_def
        self.unique: bool = True
        self.id: str = self.json_key

    def value_event( self: Self, keyvalue_event: KeyValueEvent ) -> None:
        pass

    def __repr__(self: Self) -> str:
        return f'{{ json_key: "{self.json_key}", log_key: "{self.log_key}", unique:{self.unique} }}'


class StrKeyValueSet( KeyValues[str] ):
    def __init__( self: Self, _key_def: KeyDefInterface[str] ) -> None:
        super(StrKeyValueSet, self).__init__( _key_def )

class IntKeyValueSet( KeyValues[int ] ):
    def __init__( self: Self, _key_def: KeyDefInterface[int] ) -> None:
        super(IntKeyValueSet, self).__init__( _key_def )

class BoolKeyValueSet( KeyValues[bool] ):
    def __init__( self: Self, _key_def: KeyDefInterface[bool] ) -> None:
        super(BoolKeyValueSet, self).__init__( _key_def )

class FloatKeyValueSet( KeyValues[float] ):
    def __init__( self: Self, _key_def: KeyDefInterface[float] ) -> None:
        super(FloatKeyValueSet, self).__init__( _key_def )

class TmstKeyValueSet( KeyValues[dt.datetime] ):
    def __init__( self: Self, _key_def: KeyDefInterface[dt.datetime] ) -> None:
        super(TmstKeyValueSet, self).__init__( _key_def )

