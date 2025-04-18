import multiprocessing
from typing import Self

import datetime as dt

from .. import KeyType, KeyValTypes, KeyDefInterface, AppProcessBase

from .KeyValues import KeyValues

class KeyDefBase[T: KeyValTypes ]( KeyDefInterface ):
    def __init__( self: Self, json_key: str, log_key: str, key_type: KeyType, groups: list[str] | str | None = None ) -> None:
        super(KeyDefBase, self).__init__()
        self.json_key:       str = json_key
        self.log_key:        str = log_key
        self.key_type:       KeyType = key_type
        self.groups:         list[str] | None = None
        self._skip:          bool = True
        self._event_trigger: bool = False
        self.key_values:     KeyValues[T] = KeyValues[T]( self )
        self._queue: multiprocessing.Queue | None = None

        match groups:
            case str() if groups in ["skip", ""]:
                pass
            case str():
                self.groups = [groups]
                self._skip = False
            case [] if len(groups) > 0:
                self.groups = groups
                self._skip = False

    @property
    def dologing( self: Self ) -> bool:
        return not self._skip

    @property
    def queue( self ) -> multiprocessing.Queue | None:
        if self._queue is None:
            self._queue = AppProcessBase.instance.create_queue(f"{self.key}-queue")
        return self._queue

    def visit( self: Self, visitor ) -> None:
        visitor.visit_key_def( self )


class StrKeyDef( KeyDefBase[str] ):
    def __init__( self: Self, json_key: str, log_key: str, groups: list[str ] | str | None = None ) -> None:
        super(StrKeyDef, self).__init__( json_key, log_key, KeyType.KStr, groups )

class IntKeyDef( KeyDefBase[int] ):
    def __init__( self: Self, json_key: str, log_key: str, groups: list[str ] | str | None = None ) -> None:
        super(IntKeyDef, self).__init__( json_key, log_key, KeyType.KInt, groups )

    #def add_jvalue( self: Self, jvalue: str, line_num: int ) -> AddValueResult:
    #    return self.key_values.add_value( int( jvalue ), line_num )

class BoolKeyDef( KeyDefBase[bool] ):
    def __init__( self: Self, json_key: str, log_key: str, groups: list[str ] | str | None = None ) -> None:
        super(BoolKeyDef, self).__init__( json_key, log_key, KeyType.KBool, groups )

    #def add_jvalue( self: Self, jvalue: str, line_num: int ) -> AddValueResult:
    #    return self.key_values.add_value( bool( jvalue ), line_num )

class TmstKeyDef( KeyDefBase[ dt.datetime ] ):
    very_beginning = dt.datetime.fromisoformat("1970-01-01")
    now_datetime = dt.datetime.now()

    def __init__( self, json_key: str, log_key: str, groups: list[str ] | str | None = None ) -> None:
        super(TmstKeyDef, self).__init__( json_key, log_key, KeyType.KTmst, groups )

    #def add_jvalue( self: Self, jvalue: str, line_num: int ) -> AddValueResult:
    #    try:
    #        jvalue_int = int(jvalue)
    #        datetime_value: dt.datetime = self.very_beginning + dt.timedelta( microseconds=jvalue_int )
    #        return self.key_values.add_value( datetime_value, line_num )
    #    except ValueError as e:
    #        print(f'[TmstKeyDef.add_str_value({self.json_key}:{self.log_key})] ValueError: {e} - "{jvalue}"' )
    #        return False

class FloatKeyDef( KeyDefBase[float] ):
    def __init__( self, json_key: str, log_key: str, groups: list[str ] | str | None = None ) -> None:
        super(FloatKeyDef, self).__init__( json_key, log_key, KeyType.KFloat, groups )

    #def add_jvalue( self: Self, jvalue: str, line_num: int ) -> AddValueResult:
    #    return self.key_values.add_value( float( jvalue ), line_num )

class KeyDict( dict[str, KeyDefBase ] ):
    def __init__( self: Self ) -> None:
        super(KeyDict, self).__init__()
