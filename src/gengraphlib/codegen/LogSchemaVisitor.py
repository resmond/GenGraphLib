import datetime as dt
from dataclasses import dataclass
from typing import Self

from .. import (
    KeyValueVisitorBase,
    IntKeyDef,
    IntKeyValueSet,
    BoolKeyDef,
    BoolKeyValueSet,
    FloatKeyDef,
    FloatKeyValueSet,
    TmstKeyDef,
    TmstKeyValueSet,
    StrKeyDef,
    StrKeyValueSet,
    KeyDefBase,
    KeyType,
    CmdKeyValueStream
)


@dataclass
class KeyValInfo:
    json_key: str
    log_key: str
    keytype: KeyType
    pytype_str: str
    py_type: type

class LogSchemaVisitor( KeyValueVisitorBase ):

    def __init__(self: Self, keyvalue_stream: CmdKeyValueStream ) -> None:
        super( LogSchemaVisitor, self ).__init__( keyvalue_stream )
        self.info_list: list[KeyValInfo] = []
        self.info_evt_list: list[KeyValInfo] = []
        self.evt_logged: list[KeyValInfo] = []

    def _apply( self: Self, keydef: KeyDefBase, keyval_info: KeyValInfo ) -> None:
        self.info_list.append(keyval_info)
        if keydef.dologing:
            self.info_logged.append(keyval_info)

        if "evt" in keydef.groups:
            self.info_evt_list.append(keyval_info)

    def visit_str( self: Self, keydef: StrKeyDef, keyvalues: StrKeyValueSet ) -> bool:
        self._apply( keydef, KeyValInfo( keydef.json_key, keydef.log_key, keydef.key_type, "str", str ) )
        return True

    def visit_int( self: Self, keydef: IntKeyDef, keyvalues: IntKeyValueSet ) -> bool:
        self._apply( keydef, KeyValInfo( keydef.json_key, keydef.log_key, keydef.key_type, "int", int ) )
        return True

    def visit_bool( self: Self, keydef: BoolKeyDef, keyvalues: BoolKeyValueSet ) -> bool:
        self._apply( keydef, KeyValInfo( keydef.json_key, keydef.log_key, keydef.key_type, "bool", bool ) )
        return True

    def visit_float( self: Self, keydef: FloatKeyDef, keyvalues: FloatKeyValueSet ) -> bool:
        self._apply( keydef, KeyValInfo( keydef.json_key, keydef.log_key, keydef.key_type, "float", float ) )
        return True

    def visit_tmst( self: Self, keydef: TmstKeyDef, keyvalues: TmstKeyValueSet) -> bool:
        self._apply( keydef, KeyValInfo( keydef.json_key, keydef.log_key, keydef.key_type, "dt.datetime", dt.datetime ) )
        return True

