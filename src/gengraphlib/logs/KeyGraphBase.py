import json
import os
from collections.abc import Callable
from typing import Self
from enum import IntEnum
from datetime import datetime
from sortedcontainers import SortedDict
from abc import abstractmethod

KeyValTypes: type = type[str, int, bool, datetime ]

process_fields_fn = Callable[ [ dict[str,KeyValTypes], int], int ]

class KeyType( IntEnum ):
    KStr         = 1
    KInt         = 2
    KBool        = 3
    #KTimeStamp   = 4
    KTimeStamp  = 4

class LogTimestamp:
    def __init__(self: Self, dt_str: str ) -> None:
        dt_val = datetime.fromisoformat(dt_str)
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

"""
class TmstKeyDef( KeyDefBase[datetime] ):
    def __init__( self, _json_key: str, _log_key: str ):
        super( TmstKeyDef, self ).__init__( _json_key, _log_key, KeyType.KTimeStamp )

    def add_jvalue( self: Self, jvalue: datetime, line_num: int ) -> None:
        try:
            #datetime_value = datetimemat( jvalue )
            self.key_values.add_value( jvalue, line_num )
        except ValueError as e:
            print(f'[TmstKeyDef.add_str_value({self.json_key}:{self.log_key})] ValueError: {e} - "{jvalue}"' )
"""
class TmstKeyDef( KeyDefBase[datetime ] ):
    def __init__( self, _json_key: str, _log_key: str ):
        super( TmstKeyDef, self ).__init__( _json_key, _log_key, KeyType.KTimeStamp )

    def add_jvalue( self: Self, jvalue: datetime, line_num: int ) -> None:
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

"""
    KeyGraphRootBase
"""
class KeyGraphBase( dict[str, KeyDefBase ] ):
    def __init__(self: Self, root_dir: str) -> None:
        super( KeyGraphBase, self ).__init__()
        self._root_dir = root_dir
        self._log_keys: dict[str,KeyDefBase] = dict[str,KeyDefBase]()
        self.key_groups: KeyGroups = KeyGroups(self)
        self.missing_keys: list[str] = []

    def by_logkey( self: Self, _log_key_str: str ) -> KeyDefBase:
        return self._log_keys[_log_key_str]

    def add_keydef( self: Self, _key_def: KeyDefBase ) -> None:
        self[_key_def.json_key] = _key_def
        self._log_keys[_key_def.log_key] = _key_def

    def add_keydefs( self: Self, _keydefs: list[KeyDefBase ] ) -> None:
        for _key_def in _keydefs:
            self.add_keydef(_key_def)

    def add_key_to_group( self: Self, _keygroup_name: str, _key: str ) -> None:
        key_group = self.key_groups[_keygroup_name]
        key_def: KeyDefBase = self[_key]
        key_group.add_keydef(key_def)

    def new_keygroup_with_keys( self: Self, _keygroup_name: str, _keys: list[str] ) -> None:
        self.key_groups.add_keygroup( _keygroup_name )
        for _key in _keys:
            self.add_key_to_group( _keygroup_name, _key )
        
    def process_fields( self, fields: dict[str,KeyValTypes], line_num: int ) -> bool:
        result = True

        log_key: str = ""
        json_key: str = ""
        value: KeyValTypes | None = None
        try:
            for log_key, value in fields.items():
                if log_key in self._log_keys and value is not None:
                    json_key = self._log_keys[log_key].json_key
                    self[json_key].add_jvalue( value, line_num )
                else:
                    if log_key not in self.missing_keys:
                        self.missing_keys.append( log_key )
                    result = False

        except ValueError as valexc:
            print(f"[TmstKeyDef.process_fields ({log_key}:{json_key}={value})] ValueError: {valexc}")
            result = False

        except Exception as exc:
            print(f"[TmstKeyDef.process_fields ({log_key}:{json_key}={value})] ValueError: {exc}")
            result = False
            
        return result

    def dump_key_values( self: Self ) -> None:
        for key, values_set in self.items():
            if not os.path.exists(f"/home/richard/data/jctl-logs/keys/{key}"):
                os.mkdir(f"/home/richard/data/jctl-logs/keys/{key}")

            with open(f'/home/richard/data/jctl-logs/keys/{key}/{key}.json', "w") as keyfile:
                for value_line in values_set:
                    value_line_json = json.dumps(value_line, indent=4)
                    keyfile.write(value_line_json)
                    keyfile.write("\n")

    def dump_missed_keys( self: Self ) -> None:
        data_str = json.dumps( self.missing_keys, indent=4 )
        open( "/home/richard/data/jctl-logs/missedkeys.json", "w" ).write( data_str )








