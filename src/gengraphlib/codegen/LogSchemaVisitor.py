import datetime as dt
from dataclasses import dataclass
from typing import Self

from .. import (
    KeySchemaVisitor,
    IntKeyDef,
    IntColumn,
    BoolKeyDef,
    BoolColumn,
    FloatKeyDef,
    FloatColumn,
    TmstKeyDef,
    TmstColumn,
    StrKeyDef,
    StrColumn,
    KeyDefBase,
    KeyType
)


@dataclass
class KeyValInfo:
    key: str
    alias: str
    keytype: KeyType
    pytype: type

class LogSchemaVisitor( KeySchemaVisitor ):

    def __init__( self: Self ) -> None:
        super( LogSchemaVisitor, self ).__init__()
        self.info_list: list[KeyValInfo] = []
        self.info_evt_list: list[KeyValInfo] = []
        self.evt_logged: list[KeyValInfo] = []

    def _apply( self: Self, keydef: KeyDefBase, keyval_info: KeyValInfo ) -> None:
        self.info_list.append(keyval_info)
        if keydef.dologing:
            self.info_logged.append(keyval_info)

        if "evt" in keydef.groupids:
            self.info_evt_list.append(keyval_info)

    def visit_str( self: Self, keydef: StrKeyDef, keyvalues: StrColumn ) -> bool:
        self._apply( keydef, KeyValInfo( keydef.key, keydef.alias, keydef.keytype, str ) )
        return True

    def visit_int( self: Self, keydef: IntKeyDef, keyvalues: IntColumn ) -> bool:
        self._apply( keydef, KeyValInfo( keydef.key, keydef.alias, keydef.keytype, int ) )
        return True

    def visit_bool( self: Self, keydef: BoolKeyDef, keyvalues: BoolColumn ) -> bool:
        self._apply( keydef, KeyValInfo( keydef.key, keydef.alias, keydef.keytype, bool ) )
        return True

    def visit_float( self: Self, keydef: FloatKeyDef, keyvalues: FloatColumn ) -> bool:
        self._apply( keydef, KeyValInfo( keydef.key, keydef.alias, keydef.keytype, float ) )
        return True

    def visit_tmst( self: Self, keydef: TmstKeyDef, keyvalues: TmstColumn ) -> bool:
        self._apply( keydef, KeyValInfo( keydef.key, keydef.alias, keydef.keytype, dt.datetime ) )
        return True

