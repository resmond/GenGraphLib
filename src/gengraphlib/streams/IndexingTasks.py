from typing import Self

import datetime as dt

from ..common import KeyValTypes
from ..proc.TaskLib import TaskBase, IndexTaskInterface
from ..graph.KeyDefs import (
    KeyDefBase,
    StrKeyDef,
    IntKeyDef,
    BoolKeyDef,
    FloatKeyDef,
    TmstKeyDef,
)
from ..graph.KeyValues import (
    KeyValues,
    StrKeyValueSet,
    IntKeyValueSet,
    BoolKeyValueSet,
    FloatKeyValueSet,
    TmstKeyValueSet,
)


class IndexTaskBase[ T: KeyValTypes ]( TaskBase, IndexTaskInterface ):

    def __init__(self: Self, key_def: KeyDefBase, keyvalues: KeyValues[T] ) -> None:
        super(IndexTaskBase,self).__init__( f"{key_def.key}-index" )
        self.key_def:   KeyDefBase   = key_def
        self.keyvalues: KeyValues[T] = keyvalues

    @property
    def keydef( self ) -> KeyDefBase:
        return self.key_def

    def main_loop( self: Self ) -> None:
        pass

class StrIndexingTask( IndexTaskBase[str] ):
    def __init__( self: Self, key_def: StrKeyDef, keyvalues: StrKeyValueSet ) -> None:
        super( StrIndexingTask, self ).__init__( key_def, keyvalues )

    def recv_value[str]( self: Self, rec_num: int, buffer: bytes, value: str ) -> None:
        pass

class IntIndexingTask( IndexTaskBase[int] ):
    def __init__( self: Self, key_def: IntKeyDef, keyvalues: IntKeyValueSet ) -> None:
        super( IntIndexingTask, self ).__init__( key_def, keyvalues )

    def recv_value( self: Self, rec_num: int, buffer: bytes, value: int ) -> None:
        pass

class BoolIndexingTask( IndexTaskBase[bool] ):
    def __init__( self: Self, key_def: BoolKeyDef, keyvalues: BoolKeyValueSet ) -> None:
        super( BoolIndexingTask, self ).__init__( key_def, keyvalues )

    def recv_value( self: Self, rec_num: int, buffer: bytes, value: bool ) -> None:
        pass

class FloatIndexingTask( IndexTaskBase[float] ):
    def __init__( self: Self, key_def: FloatKeyDef, keyvalues: FloatKeyValueSet ) -> None:
        super( FloatIndexingTask, self ).__init__( key_def, keyvalues )

    def recv_value( self: Self, rec_num: int, buffer: bytes, value: float ) -> None:
        pass

class TmstIndexingTask( IndexTaskBase[dt.datetime] ):
    def __init__( self: Self, key_def: TmstKeyDef, keyvalues: TmstKeyValueSet ) -> None:
        super( TmstIndexingTask, self ).__init__( key_def, keyvalues )

    def recv_value( self: Self, rec_num: int, buffer: bytes, value: dt.datetime ) -> bool:
        pass
