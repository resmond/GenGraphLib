from typing import Self

import datetime as dt
from abc import abstractmethod, ABC
from enum import IntEnum

from .. import KeyValTypes
from .KeyValues import KeyValueBase

class KeyType( IntEnum ):
    KStr         = 1
    KInt         = 2
    KBool        = 3
    KTimeStamp  = 4

class KeyDefBase[ T: KeyValTypes]( ABC ):
    def __init__( self: Self, _json_key: str, _log_key: str, _key_type: KeyType, groups: list[str] | str | None = None) -> None:
        self.json_key: str = _json_key
        self.log_key: str = _log_key
        self.key_type: KeyType = _key_type
        self.groups: list[str] | None = None
        self.skip: bool = False
        self.key_values: KeyValueBase[T] = KeyValueBase[T ]()

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

    def add_value( self: Self, new_value: T, line_num: int ) -> None:
        self.key_values.add_value(new_value, line_num)

    @property
    def dologing( self ) -> bool:
        return not self.skip

    @abstractmethod
    def add_jvalue( self: Self, jvalue: KeyValTypes, line_num: int ) -> None:
        pass

class StrKeyDef( KeyDefBase[str] ):
    def __init__( self, _json_key: str, _log_key: str, groups: list[str] | str | None = None ):
        super( StrKeyDef, self ).__init__( _json_key, _log_key, KeyType.KStr, groups )

    def add_jvalue( self: Self, jvalue: str, line_num: int ) -> None:
        self.key_values.add_value( jvalue, line_num )

class IntKeyDef( KeyDefBase[int] ):
    def __init__( self, _json_key: str, _log_key: str, groups: list[str] | str  | None = None ):
        super( IntKeyDef, self ).__init__( _json_key, _log_key, KeyType.KInt, groups )

    def add_jvalue( self: Self, jvalue: str, line_num: int ) -> None:
        self.key_values.add_value( int( jvalue ), line_num )

class BoolKeyDef( KeyDefBase[bool] ):
    def __init__( self, _json_key: str, _log_key: str, groups: list[str] | str  | None = None ):
        super( BoolKeyDef, self ).__init__( _json_key, _log_key, KeyType.KBool, groups )

    def add_jvalue( self: Self, jvalue: str, line_num: int ) -> None:
        self.key_values.add_value( bool( jvalue ), line_num )

class TmstKeyDef( KeyDefBase[dt.datetime ] ):
    def __init__( self, _json_key: str, _log_key: str, groups: list[str] | str  | None = None ):
        super( TmstKeyDef, self ).__init__( _json_key, _log_key, KeyType.KTimeStamp, groups )

    def add_jvalue( self: Self, jvalue: dt.datetime, line_num: int ) -> None:
        try:
            #            datetime_value = datetime( jvalue )
            self.key_values.add_value( jvalue, line_num )
        except ValueError as e:
            print(f'[TmstKeyDef.add_str_value({self.json_key}:{self.log_key})] ValueError: {e} - "{jvalue}"' )



