from typing import Self

import datetime as dt

from . import KeyDefBase, KeyValues

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

