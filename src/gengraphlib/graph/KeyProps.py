from __future__ import annotations

from abc import ABC
from typing import Self

from src.gengraphlib import KeyValTypes, KeyDefBase, KeyType, AddValueResult

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
class KeyPropBase[KT: KeyValTypes ]( KeyDefBase[ KT ], ABC ):
    def __init__(self: Self, _json_key: str, _log_key: str, _key_type: KeyType, groups: list[str] | str | None = None) -> None:
        super().__init__( _json_key, _log_key, _key_type, groups )
        self._desc_name: str | None = None

    def __set_name__(self: Self, owner: type, name: str):
        print(f"[StrKeyProp({self.json_key})].__set_name__( owner:{type(owner).__name__} )" )
        self._desc_name = name
        return self.json_key

    def __set__(self: Self, instance: type, value: str ):
        print(f"[StrKeyProp({self._desc_name}).__set__( instance:{type(instance).__name__} value[{type(value)}]: {value})" )
        #return self.json_key

    def __delete__(self, instance) -> None:
        print(f'MetaDescriptorBase[{self._desc_name}]__set__( instance: {type(instance)} )')
        pass

    def __get__(self, instance, owner) -> str | None:
        print(f'MetaDescriptorBase[{self._desc_name}]__set__( instance: {type(instance)}, owner:{type(owner)} )')
        return self.json_key


"""
    KeyDefPropBase

"""


"""
    StrKeyProp

"""
class StrKeyProp( KeyPropBase[str] ):
    def __init__( self, _json_key: str, _log_key: str, groups: list[str] | str | None = None ):
        super().__init__(_json_key, _log_key, KeyType.KStr,  groups )
        self._desc_name: str = ""
        #self._key_def: StrKeyDef = StrKeyDef( _json_key, _log_key, groups )

    def add_jvalue( self: Self, jvalue: str, line_num: int ) -> AddValueResult:
        val_result: AddValueResult = self.key_values.add_value( jvalue, line_num )
        if val_result is None:
            return val_result
        else:
            return self.on_trigger( val_result )

    def on_trigger( self: Self, val_result: AddValueResult ) -> AddValueResult:

        print(f"[StrKeyProp.on_trigger] {self.json_key}")
        return val_result
