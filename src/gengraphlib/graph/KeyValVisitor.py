from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Self

from typing_extensions import TypeVar

from . import (
    KeyDefBase,
    KeyValues,
    StrKeyDef,
    StrKeyValueSet,
    IntKeyDef,
    IntKeyValueSet,
    BoolKeyDef,
    BoolKeyValueSet,
    FloatKeyDef,
    FloatKeyValueSet,
    TmstKeyDef,
    TmstKeyValueSet
)

from .. import CmdKeyValueStream

KeyDefType = TypeVar( 'KeyDefType', bound=KeyDefBase )
KeyValType = TypeVar( 'KeyValType', bound=KeyValues )

keydef_visit = Callable[ [ KeyDefType, KeyValType ], bool ]

class KeyValueVisitorBase( ABC ):

    def __init__(self: Self, keyvalue_stream: CmdKeyValueStream ) -> None:
        super( KeyValueVisitorBase, self ).__init__()
        self.keyvalue_stream: CmdKeyValueStream = keyvalue_stream

    @abstractmethod
    def visit_str( self: Self, keydef: StrKeyDef, keyvalues: StrKeyValueSet ) -> bool:
        pass

    @abstractmethod
    def visit_int( self: Self, keydef: IntKeyDef, keyvalues: IntKeyValueSet ) -> bool:
        pass

    @abstractmethod
    def visit_bool( self: Self, keydef: BoolKeyDef, keyvalues: BoolKeyValueSet ) -> bool:
        pass

    @abstractmethod
    def visit_float( self: Self, keydef: FloatKeyDef, keyvalues: FloatKeyValueSet ) -> bool:
        pass

    @abstractmethod
    def visit_tmst( self: Self, keydef: TmstKeyDef, keyvalues: TmstKeyValueSet ) -> bool:
        pass

