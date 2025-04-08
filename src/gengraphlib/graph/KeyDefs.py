from __future__ import annotations
from typing import Self, Protocol

import datetime as dt
from abc import abstractmethod, ABC
from enum import IntEnum

from .. import KeyValTypes
from .KeyValues import KeyValueBase, AddValueResult, KeyValueTriggerBase


class KeyType( IntEnum ):
    KStr         = 1
    KInt         = 2
    KBool        = 3
    KTimeStamp  = 4

class KeyDefBase[T: KeyValTypes]( ABC ):
    def __init__( self: Self, _json_key: str, _log_key: str, _key_type: KeyType, groups: list[str] | str | None = None) -> None:
        self.json_key: str = _json_key
        self.log_key: str = _log_key
        self.key_type: KeyType = _key_type
        self.groups: list[str] | None = None
        self.skip: bool = False
        self.event_trigger: bool = False
        self.key_values: KeyValueBase[T] = KeyValueBase[T]( _json_key )

        if groups is str:
            if groups == "skip":
                self.skip = True
            self.groups = [groups]
        if groups is not None:
            self.groups: list[str] = groups
            if "skip" in self.groups:
                self.skip = True
        else:
            self.groups = None

        super(KeyDefBase, self).__init__()

    def add_trigger( self: Self, trigger: KeyValueTriggerBase[T] ) -> None:
        self.key_values.add_trigger( trigger )
        self.event_trigger = True

    def add_value( self: Self, new_value: T, line_num: int ) -> AddValueResult:
        addval_result: AddValueResult = self.key_values.add_value(new_value, line_num)
        if addval_result is None:
            return addval_result
        else:
            return addval_result

    @property
    def dologing( self ) -> bool:
        return not self.skip

    @abstractmethod
    def add_jvalue( self: Self, jvalue: KeyValTypes, line_num: int ) -> AddValueResult:
        pass



"""--------------------------------------------------------
    StrKeyDef

"""
class StrKeyDef( KeyDefBase[str] ):
    def __init__( self, _json_key: str, _log_key: str, groups: list[str] | str | None = None ):
        super( StrKeyDef, self ).__init__( _json_key, _log_key, KeyType.KStr, groups )

    def add_jvalue( self: Self, jvalue: str, line_num: int ) -> AddValueResult:
        return self.key_values.add_value( jvalue, line_num )


"""--------------------------------------------------------

    IntKeyDef

"""
class IntKeyDef( KeyDefBase[int] ):
    def __init__( self, _json_key: str, _log_key: str, groups: list[str] | str  | None = None ):
        super( IntKeyDef, self ).__init__( _json_key, _log_key, KeyType.KInt, groups )

    def add_jvalue( self: Self, jvalue: str, line_num: int ) -> AddValueResult:
        return self.key_values.add_value( int( jvalue ), line_num )

"""--------------------------------------------------------
    BoolKeyDef

"""
class BoolKeyDef( KeyDefBase[bool] ):
    def __init__( self, _json_key: str, _log_key: str, groups: list[str] | str  | None = None ):
        super( BoolKeyDef, self ).__init__( _json_key, _log_key, KeyType.KBool, groups )

    def add_jvalue( self: Self, jvalue: str, line_num: int ) -> AddValueResult:
        return self.key_values.add_value( bool( jvalue ), line_num )

"""
    TmstKeyDef

"""
class TmstKeyDef( KeyDefBase[ dt.datetime ] ):
    def __init__( self, _json_key: str, _log_key: str, groups: list[str] | str  | None = None ):
        super( TmstKeyDef, self ).__init__( _json_key, _log_key, KeyType.KTimeStamp, groups )

    def add_jvalue( self: Self, jvalue: str, line_num: int ) -> AddValueResult:
        try:
            datetime_value: dt.datetime = dt.datetime.fromordinal(int(jvalue))
            return self.key_values.add_value( datetime_value, line_num )
        except ValueError as e:
            print(f'[TmstKeyDef.add_str_value({self.json_key}:{self.log_key})] ValueError: {e} - "{jvalue}"' )
            return False

class KeyPropRepository(ABC):
    def __init__(self) -> None:
        super(KeyPropRepository, self).__init__()
        self.keyprops_list: list[KeyPropBase] = list[KeyPropBase]()

    def add_keyprop(self, key_prop: KeyPropBase) -> None:
        self.keyprops_list.append( key_prop )

    def keyprops_init(self):
        pass

    def __init_subclass__( cls ):
        super().__init_subclass__( cls )

##################################### KeyDefProps #########################################
"""
    KeyDefPropBase

"""
class KeyPropBase[ KT: KeyValTypes ]( KeyDefBase[KT], ABC ):

    def __init__( self, key_repository: KeyPropRepository, _json_key: str, _log_key: str, _key_type: KeyType, groups: list[str ] | None = None ):
        self.key_repository: KR = key_repository
        self.key_repository_type: type = type(self.key_repository)
        self.key_repository_cls = key_repository.__class__
        super( KeyPropBase, self ).__init__( _json_key, _log_key, _key_type, groups )

class KeyPropClassSurface( Protocol ):

    def keyprops_init( self ):
        pass

"""
    StrKeyProp

"""
class StrKeyProp( KeyPropBase[str] ):
    def __init__( self, class_surface: KeyPropClassSurface, key_repository: KeyPropRepository, _json_key: str, _log_key: str, groups: list[str ] | str | None = None ):
        self.class_surface = class_surface
        super( StrKeyProp, self ).__init__( key_repository=key_repository, _json_key=_json_key, _log_key = _log_key, _key_type = KeyType.KStr, groups=groups )
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

