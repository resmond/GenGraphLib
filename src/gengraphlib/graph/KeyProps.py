from __future__ import annotations
from typing import Protocol, Self
from abc import ABC

from src.gengraphlib import KeyValTypes
from .KeyDefs import KeyDefBase, KeyType
from .KeyValues import AddValueResult

class KeyPropRepository(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.keyprops_list: list[KeyPropBase] = list[KeyPropBase]()

    def add_keyprop(self, key_prop: KeyPropBase) -> None:
        self.keyprops_list.append( key_prop )

    def keyprops_init(self):
        pass

#    def __init_subclass__( cls ):
#        super().__init_subclass__()

##################################### KeyDefProps #########################################
"""
    KeyDefPropBase

"""
class KeyPropBase[ KT: KeyValTypes ]( KeyDefBase[KT], ABC ):

    def __init__( self, key_repository: KeyPropRepository, _json_key: str, _log_key: str, _key_type: KeyType, groups: list[str ] | None = None ):
        super().__init__( _json_key, _log_key, _key_type, groups )
        self.key_repository: KeyPropRepository = key_repository

class KeyPropClassSurface( Protocol ):

    def keyprops_init( self ):
        pass

"""
    StrKeyProp

"""
class StrKeyProp( KeyPropBase[str] ):
    def __init__( self, class_surface: KeyPropClassSurface, key_repository: KeyPropRepository, _json_key: str, _log_key: str, groups: list[str ] | str | None = None ):
        super().__init__( key_repository=key_repository, _json_key=_json_key, _log_key = _log_key, _key_type = KeyType.KStr, groups=groups )
        self.class_surface = class_surface
        if self == self.key_repository:
            print("self is same")


    def add_jvalue( self: Self, jvalue: str, line_num: int ) -> AddValueResult:
        val_result: AddValueResult = self.key_values.add_value( jvalue, line_num )
        if val_result is None:
            return val_result
        else:
            return self.on_trigger(self.class_surface, val_result)

    def on_trigger( self: Self, class_surface: KeyPropClassSurface, val_result: AddValueResult ) -> AddValueResult:

        if class_surface == self.key_repository:
            print("host same as class_repor")

        print(f"[StrKeyProp.on_trigger] {self.json_key}")
        return val_result
