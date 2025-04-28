from dataclasses import dataclass
from typing import Self

from .. import (
    KeySchemaVisitor,
    IntKeyDef,
    BoolKeyDef,
    FloatKeyDef,
    TmstKeyDef,
    StrKeyDef,
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
        self.info_list:     list[KeyValInfo] = []
        self.info_evt_list: list[KeyValInfo] = []
        self.evt_logged:    list[KeyValInfo] = []

    def _apply( self: Self, keydef: KeyDefBase ) -> None:
        pass
        # self.info_list.append(keyval_info)
        # if keydef.dologing:
        #     self.info_logged.append(keyval_info)
        #
        # if "evt" in keydef.groupids:
        #     self.info_evt_list.append(keyval_info)

    def visit_str( self: Self, keydef: StrKeyDef ) -> bool:
        self._apply( keydef  )
        return True

    def visit_int( self: Self, keydef: IntKeyDef ) -> bool:
        self._apply( keydef )
        return True

    def visit_bool( self: Self, keydef: BoolKeyDef ) -> bool:
        self._apply( keydef )
        return True

    def visit_float( self: Self, keydef: FloatKeyDef ) -> bool:
        self._apply( keydef )
        return True

    def visit_tmst( self: Self, keydef: TmstKeyDef ) -> bool:
        self._apply( keydef  )
        return True

