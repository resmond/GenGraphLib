from typing import Self
from typing import Protocol

from ..graph import (
    StrKeyDef,
    IntKeyDef,
    BoolKeyDef,
    FloatKeyDef,
    TmstKeyDef
)

# from ..columns import (
#     StrColumn,
#     IntColumn,
#     BoolColumn,
#     FloatColumn,
#     TmstColumn
# )

class KeySchemaVisitor[ TReturn ]( Protocol ):

    def visit_str( self: Self, keydef: StrKeyDef ) -> TReturn: ...
    def visit_int( self: Self, keydef: IntKeyDef ) -> TReturn: ...
    def visit_bool( self: Self, keydef: BoolKeyDef ) -> TReturn: ...
    def visit_float( self: Self, keydef: FloatKeyDef ) -> TReturn: ...
    def visit_tmst( self: Self, keydef: TmstKeyDef ) -> TReturn: ...

