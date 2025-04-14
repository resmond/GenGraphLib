from typing import Self

import datetime as dt

from .. import KeyType
from . import KeyDefBase

"""   StrKeyDef

"""
class StrKeyDef( KeyDefBase[str] ):
    def __init__( self: Self, _json_key: str, _log_key: str, groups: list[str] | str | None = None ) -> None:
        super(StrKeyDef, self).__init__( _json_key, _log_key, KeyType.KStr, groups )

    #def add_jvalue( self: Self, jvalue: str, line_num: int ) -> AddValueResult:
    #    return self.key_values.add_value( jvalue, line_num )

"""   IntKeyDef

"""
class IntKeyDef( KeyDefBase[int] ):
    def __init__( self: Self, _json_key: str, _log_key: str, groups: list[str] | str  | None = None ) -> None:
        super(IntKeyDef, self).__init__( _json_key, _log_key, KeyType.KInt, groups )

    #def add_jvalue( self: Self, jvalue: str, line_num: int ) -> AddValueResult:
    #    return self.key_values.add_value( int( jvalue ), line_num )

"""
    BoolKeyDef

"""
class BoolKeyDef( KeyDefBase[bool] ):
    def __init__( self: Self, _json_key: str, _log_key: str, groups: list[str] | str  | None = None ) -> None:
        super(BoolKeyDef, self).__init__( _json_key, _log_key, KeyType.KBool, groups )

    #def add_jvalue( self: Self, jvalue: str, line_num: int ) -> AddValueResult:
    #    return self.key_values.add_value( bool( jvalue ), line_num )

"""
    TmstKeyDef

"""
class TmstKeyDef( KeyDefBase[ dt.datetime ] ):
    very_beginning = dt.datetime.fromisoformat("1970-01-01")
    now_datetime = dt.datetime.now()

    def __init__( self, _json_key: str, _log_key: str, groups: list[str] | str  | None = None ) -> None:
        super(TmstKeyDef, self).__init__( _json_key, _log_key, KeyType.KTimeStamp, groups )

    #def add_jvalue( self: Self, jvalue: str, line_num: int ) -> AddValueResult:
    #    try:
    #        jvalue_int = int(jvalue)
    #        datetime_value: dt.datetime = self.very_beginning + dt.timedelta( microseconds=jvalue_int )
    #        return self.key_values.add_value( datetime_value, line_num )
    #    except ValueError as e:
    #        print(f'[TmstKeyDef.add_str_value({self.json_key}:{self.log_key})] ValueError: {e} - "{jvalue}"' )
    #        return False

"""
    FloatKeyDef

"""
class FloatKeyDef( KeyDefBase[float] ):
    def __init__( self, _json_key: str, _log_key: str, groups: list[str] | str  | None = None ) -> None:
        super(FloatKeyDef, self).__init__( _json_key, _log_key, KeyType.KFloat, groups )

    #def add_jvalue( self: Self, jvalue: str, line_num: int ) -> AddValueResult:
    #    return self.key_values.add_value( float( jvalue ), line_num )

class KeyDict( dict[str, KeyDefBase ] ):
    def __init__( self: Self ) -> None:
        super(KeyDict, self).__init__()
