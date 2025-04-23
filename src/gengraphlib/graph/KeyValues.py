from typing import Self

import os
import datetime as dt

from sortedcontainers import SortedDict

from .. import (
    KeyType,
    KeyValTypes,
    LineRefList
)

from .. import (
    KeyDefInterface,
    KeyValuesInterface,
    KeyValueEvent
)

#from .. import GNodeInterface

class KeyValues[T: KeyValTypes]( SortedDict[T, LineRefList], KeyValuesInterface ):
    def __init__(self: Self, _key_def: KeyDefInterface, index_dir: str) -> None:
        super(KeyValues, self).__init__()
        self.key_def: KeyDefInterface = _key_def
        self.index_dir: str = index_dir
        self.id: str = _key_def.key
        self.keytype: KeyType
        self.unique: bool = True

    def init_index( self ) -> bool:
        try:
            os.mkdir( self.index_dir )
            return True

        except Exception as exc:
            print(f"KeyValues[{self.id}] root_dir: {self.index_dir} Exception: {exc}")
            return False

    def value_event( self: Self, keyvalue_event: KeyValueEvent ) -> None:
        pass

    def __repr__(self: Self) -> str:
        return f'{{ json_key: "{self.json_key}", log_key: "{self.log_key}", unique:{self.unique} }}'

class StrKeyValueSet( KeyValues[str] ):
    def __init__( self: Self, _key_def: KeyDefInterface ) -> None:
        super(StrKeyValueSet, self).__init__( _key_def )

class IntKeyValueSet( KeyValues[int ] ):
    def __init__( self: Self, _key_def: KeyDefInterface ) -> None:
        super(IntKeyValueSet, self).__init__( _key_def )

class BoolKeyValueSet( KeyValues[bool] ):
    def __init__( self: Self, _key_def: KeyDefInterface ) -> None:
        super(BoolKeyValueSet, self).__init__( _key_def )

class FloatKeyValueSet( KeyValues[float] ):
    def __init__( self: Self, _key_def: KeyDefInterface ) -> None:
        super(FloatKeyValueSet, self).__init__( _key_def )

class TmstKeyValueSet( KeyValues[dt.datetime] ):
    def __init__( self: Self, _key_def: KeyDefInterface ) -> None:
        super(TmstKeyValueSet, self).__init__( _key_def )

