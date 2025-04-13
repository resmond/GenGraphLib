from __future__ import annotations

from typing import Self

from src.gengraphlib import KeyValTypes, KeyDefBase, KeyType

"""
class KeyPropRepository(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.keyprops_list: list[KeyPropBase] = list[KeyPropBase]()

    def add_keyprop(self, key_prop: KeyPropBase) -> None:
        self.keyprops_list.append( key_prop )

    def keyprops_init(self):
        pass
"""

##################################### KeyDefProps #########################################
class KeyPropBase[ T: KeyValTypes ]( KeyDefBase[ T ] ):
    def __init__(self: Self, _json_key: str, _log_key: str, _key_type: KeyType, groups: list[str] | str | None = None) -> None:
        super(KeyPropBase, self).__init__( _json_key, _log_key, _key_type, groups )
        self._desc_name: str | None = None

"""
    KeyDefPropBase

"""


"""
    StrKeyProp

"""
class StrKeyProp( KeyPropBase[str] ):
    def __init__( self, _json_key: str, _log_key: str, groups: list[str] | str | None = None ) -> None:
        super(StrKeyProp, self).__init__(_json_key, _log_key, KeyType.KStr, groups )

    #def add_jvalue( self: Self, jvalue: str, line_num: int ) -> AddValueResult:
    #    val_result: AddValueResult = self.key_values.add_value( jvalue, line_num )
    #    if val_result is None:
    #        return val_result
    #    else:
    #        return self.on_trigger( val_result )

"""
    def on_trigger( self: Self, val_result: AddValueResult ) -> AddValueResult:

        print(f"[StrKeyProp.on_trigger] {self.json_key}")
        return val_result
"""