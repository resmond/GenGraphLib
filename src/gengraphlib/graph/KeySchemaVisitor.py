import typing as typing
import collections.abc as collabc
from asyncio import Protocol

from src.gengraphlib.graph import (
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

#from src.gengraphlib import CmdKeyValueStream

#KeyDefType = TypeVar( 'KeyDefType', bound=KeyDefBase )
#KeyValType = TypeVar( 'KeyValType', bound=KeyValues )
#keydef_visit = Callable[ [ KeyDefType, KeyValType ], bool ]

keydef_visit = collabc.Callable[ [ KeyDefBase, KeyValues ], bool ]

KeyValuePair: type = tuple[str, KeyDefBase, KeyValues]
KeyValueIterator: type = collabc.AsyncIterator[KeyValuePair]
KeyValueGenerator: type = collabc.AsyncGenerator[KeyValueIterator, None]
#CmdKeyValueStream = aio.StreamReader

class KeySchemaVisitor[ TReturn ]( Protocol ):

    def __init__( self: typing.Self ) -> None: ...

    def visit_str( self: typing.Self, keydef: StrKeyDef, keyvalues: StrKeyValueSet ) -> TReturn: ...
    def visit_int( self: typing.Self, keydef: IntKeyDef, keyvalues: IntKeyValueSet ) -> TReturn: ...
    def visit_bool( self: typing.Self, keydef: BoolKeyDef, keyvalues: BoolKeyValueSet ) -> TReturn: ...
    def visit_float( self: typing.Self, keydef: FloatKeyDef, keyvalues: FloatKeyValueSet ) -> TReturn: ...
    def visit_tmst( self: typing.Self, keydef: TmstKeyDef, keyvalues: TmstKeyValueSet ) -> TReturn: ...

