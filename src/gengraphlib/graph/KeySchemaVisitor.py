from typing import Self
from typing import Protocol

from ..graph import (
    StrKeyDef,
    IntKeyDef,
    BoolKeyDef,
    FloatKeyDef,
    TmstKeyDef
)

from ..columns import (
    StrKeyValueSet,
    IntKeyValueSet,
    BoolKeyValueSet,
    FloatKeyValueSet,
    TmstKeyValueSet
)

class KeySchemaVisitor[ TReturn ]( Protocol ):

    def visit_str( self: Self, keydef: StrKeyDef, keyvalues: StrKeyValueSet ) -> TReturn: ...
    def visit_int( self: Self, keydef: IntKeyDef, keyvalues: IntKeyValueSet ) -> TReturn: ...
    def visit_bool( self: Self, keydef: BoolKeyDef, keyvalues: BoolKeyValueSet ) -> TReturn: ...
    def visit_float( self: Self, keydef: FloatKeyDef, keyvalues: FloatKeyValueSet ) -> TReturn: ...
    def visit_tmst( self: Self, keydef: TmstKeyDef, keyvalues: TmstKeyValueSet ) -> TReturn: ...

