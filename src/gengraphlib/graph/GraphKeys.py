from abc import abstractmethod
from typing import Self

import datetime as dt

from enum import IntEnum

from collections.abc import Callable

from sortedcontainers import SortedDict

KeyValTypes: type = type[str, int, bool, dt.datetime ]

process_fields_fn = Callable[ [ dict[str,KeyValTypes], int, str | None], int ]

class KeyType( IntEnum ):
    KStr         = 1
    KInt         = 2
    KBool        = 3
    KTimeStamp  = 4

class LogTimestamp:
    def __init__(self: Self, dt_str: str ) -> None:
        dt_val = dt.datetime.fromisoformat(dt_str)
        super( LogTimestamp, self ).__init__( dt_val )

class LineRefList( list[ (str, int) ] ):
    pass

class KeyValueInstancesBase[ T: KeyValTypes ]( SortedDict[ T, LineRefList ] ):
    def __init__(self: Self) -> None:
        super().__init__()
        self.unique: bool = True
        self._cnt: int = 0

    def add_value( self: Self, new_value: T, line_num: int ) -> None:
        if new_value not in self:
            self[new_value] = []
        else:
            self.unique = False

        self[new_value].append( line_num )
        self._cnt += 1

class KeyDefBase[ T: KeyValTypes ]( KeyValueInstancesBase[T] ):
    def __init__( self: Self, _json_key: str, _log_key: str, _key_type: KeyType) -> None:
        super(KeyDefBase, self ).__init__()
        self.json_key: str = _json_key
        self.log_key: str = _log_key
        self.key_type: KeyType = _key_type
        self.key_values: KeyValueInstancesBase[T] = KeyValueInstancesBase[T]()

    def add_value( self: Self, new_value: T, line_num: int ) -> None:
        self.key_values.add_value(new_value, line_num)

    @abstractmethod
    def add_jvalue( self: Self, jvalue: KeyValTypes, line_num: int ) -> None:
        pass

class StrKeyDef( KeyDefBase[str] ):
    def __init__( self, _json_key: str, _log_key: str ):
        super( StrKeyDef, self ).__init__( _json_key, _log_key, KeyType.KStr )

    def add_jvalue( self: Self, jvalue: str, line_num: int ) -> None:
        self.key_values.add_value( jvalue, line_num )

class IntKeyDef( KeyDefBase[int] ):
    def __init__( self, _json_key: str, _log_key: str ):
        super( IntKeyDef, self ).__init__( _json_key, _log_key, KeyType.KInt )

    def add_jvalue( self: Self, jvalue: str, line_num: int ) -> None:
        self.key_values.add_value( int( jvalue ), line_num )

class BoolKeyDef( KeyDefBase[bool] ):
    def __init__( self, _json_key: str, _log_key: str ):
        super( BoolKeyDef, self ).__init__( _json_key, _log_key, KeyType.KBool )

    def add_jvalue( self: Self, jvalue: str, line_num: int ) -> None:
        self.key_values.add_value( bool( jvalue ), line_num )

class TmstKeyDef( KeyDefBase[dt.datetime ] ):
    def __init__( self, _json_key: str, _log_key: str ):
        super( TmstKeyDef, self ).__init__( _json_key, _log_key, KeyType.KTimeStamp )

    def add_jvalue( self: Self, jvalue: dt.datetime, line_num: int ) -> None:
        try:
            #            datetime_value = datetime( jvalue )
            self.key_values.add_value( jvalue, line_num )
        except ValueError as e:
            print(f'[TmstKeyDef.add_str_value({self.json_key}:{self.log_key})] ValueError: {e} - "{jvalue}"' )

class KeyGroup( list[KeyDefBase] ):
    def __init__( self: Self, keygroup_name: str ) -> None:
        super( KeyGroup, self ).__init__()
        self.keygroup_name: str = keygroup_name

    def add_keydef(self: Self, other: KeyDefBase) -> None:
        self.append(other)

class KeyGroups( dict[str, KeyGroup ] ):
    def __init__( self: Self, graph_root: dict[str,KeyDefBase ] ) -> None:
        super(KeyGroups, self).__init__()
        self.graph_root: dict[str,KeyDefBase ] = graph_root

    def add_keygroup( self: Self, keygroup_name: str ) -> None:
        self[keygroup_name] = KeyGroup( keygroup_name )

    def add_key_to_group( self: Self, _keygroup_name: str, _key_def: KeyDefBase ) -> None:
        key_group: KeyGroup = self[_keygroup_name]
        key_group.add_keydef(_key_def)

    def add_keys_to_group( self: Self, _keygroup_name: str, keys: list[str]) -> None:
        for _json_key in keys:
            _key_def = self.graph_root[_json_key]
            self.add_key_to_group( _keygroup_name, _key_def )

class DefaultDictOfLists(dict[str, list[str] ]):

    def __init__( self: Self ) -> None:
        super(DefaultDictOfLists, self).__init__()

    def add_entry( self: Self, key: str, value: str ) -> None:

        if key not in self:
            self[key] = []

        self[key].append( value )

