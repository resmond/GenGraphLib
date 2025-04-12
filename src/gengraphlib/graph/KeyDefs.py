from __future__ import annotations
from typing import Self

import datetime as dt
from abc import abstractmethod

from src.gengraphlib import KeyValTypes, KeyType
from .KeyValues import KeyValues, AddValueResult, KeyValueTriggerBase

class KeyDefBase[T: KeyValTypes]:
    def __init__( self: Self, _json_key: str, _log_key: str, _key_type: KeyType, groups: list[str] | str | None = None) -> None:
        super().__init__()
        self.json_key: str = _json_key
        self.log_key: str = _log_key
        self.key_type: KeyType = _key_type
        self.groups: list[str] | None = None
        self._skip: bool = True
        self._event_trigger: bool = False
        self.key_values: KeyValues[T] = KeyValues[T]( self )

        match groups:
            case str() if groups in ["skip", ""]:
                pass
            case str():
                self.groups = [groups]
                self._skip = False
            case [] if len(groups) > 0:
                self.groups = groups
                self._skip = False

        super().__init__()

    def add_trigger( self: Self, trigger: KeyValueTriggerBase[T] ) -> None:
        self.key_values.add_trigger( trigger )
        self._event_trigger = True
        self._skip = False

    def add_value( self: Self, new_value: T, line_num: int ) -> AddValueResult:
        if self._skip:
            return None
        else:
            return self.key_values.add_value(new_value, line_num)

    @property
    def dologing( self: Self ) -> bool:
        return not self._skip

    @abstractmethod
    def add_jvalue( self: Self, jvalue: KeyValTypes, line_num: int ) -> AddValueResult:
        pass

"""   StrKeyDef

"""
class StrKeyDef( KeyDefBase[str] ):
    def __init__( self, _json_key: str, _log_key: str, groups: list[str] | str | None = None ):
        super().__init__( _json_key, _log_key, KeyType.KStr, groups )

    def add_jvalue( self: Self, jvalue: str, line_num: int ) -> AddValueResult:
        return self.key_values.add_value( jvalue, line_num )

"""   IntKeyDef

"""
class IntKeyDef( KeyDefBase[int] ):
    def __init__( self, _json_key: str, _log_key: str, groups: list[str] | str  | None = None ):
        super().__init__( _json_key, _log_key, KeyType.KInt, groups )

    def add_jvalue( self: Self, jvalue: str, line_num: int ) -> AddValueResult:
        return self.key_values.add_value( int( jvalue ), line_num )

"""
    BoolKeyDef

"""
class BoolKeyDef( KeyDefBase[bool] ):
    def __init__( self, _json_key: str, _log_key: str, groups: list[str] | str  | None = None ):
        super().__init__( _json_key, _log_key, KeyType.KBool, groups )

    def add_jvalue( self: Self, jvalue: str, line_num: int ) -> AddValueResult:
        return self.key_values.add_value( bool( jvalue ), line_num )

"""
    TmstKeyDef

"""
class TmstKeyDef( KeyDefBase[ dt.datetime ] ):
    very_beginning = dt.datetime.fromisoformat("1970-01-01")
    now_datetime = dt.datetime.now()

    def __init__( self, _json_key: str, _log_key: str, groups: list[str] | str  | None = None ):
        super().__init__( _json_key, _log_key, KeyType.KTimeStamp, groups )

    def add_jvalue( self: Self, jvalue: str, line_num: int ) -> AddValueResult:
        try:
            jvalue_int = int(jvalue)
            datetime_value: dt.datetime = self.very_beginning + dt.timedelta( microseconds=jvalue_int )
            return self.key_values.add_value( datetime_value, line_num )
        except ValueError as e:
            print(f'[TmstKeyDef.add_str_value({self.json_key}:{self.log_key})] ValueError: {e} - "{jvalue}"' )
            return False

"""
    FloatKeyDef

"""
class FloatKeyDef( KeyDefBase[float] ):
    def __init__( self, _json_key: str, _log_key: str, groups: list[str] | str  | None = None ):
        super().__init__( _json_key, _log_key, KeyType.KFloat, groups )

    def add_jvalue( self: Self, jvalue: str, line_num: int ) -> AddValueResult:
        return self.key_values.add_value( float( jvalue ), line_num )

