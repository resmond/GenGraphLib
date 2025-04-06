from typing import Self, Any

import json
import os

from .GraphKeyDefs import (
    KeyDefBase,
    KeyGroups,
    KeyRepository,
    KeyDefIndex
)

"""
    DefaultDictOfLists
"""
class DefaultDictOfLists(dict[str, list[str]]):

    def __init__( self: Self ) -> None:
        super(DefaultDictOfLists, self).__init__()

    def add_entry( self: Self, key: str, value: str ) -> None:

        if key not in self:
            self[key] = []

        self[key].append( value )

"""
    KeyGraphBase
"""
class KeyGraphBase( KeyRepository ):
    def __init__(self: Self, root_dir: str) -> None:
        super( KeyGraphBase, self ).__init__(root_dir)
        self._log_keys: KeyDefIndex = KeyDefIndex()
        self.none_values: DefaultDictOfLists = DefaultDictOfLists()
        self.missing_keys: list[str] = []
        #self.message_fields: DefaultDictOfLists = DefaultDictOfLists()

    def by_logkey( self: Self, _log_key_str: str ) -> KeyDefBase:
        return self._log_keys[_log_key_str]

    def process_field( self: Self, log_key: str, value: Any, line_num: int, log_line: str = "" ) -> bool:
        result: bool = False

        json_key = self._log_keys[log_key].json_key

        if value is None:
            self.none_values.add_entry( log_key, log_line )

        elif log_key in self._log_keys:
            try:
                match type(value).__name__:
                    case "list":
                        str_val = str(value)
                        self[json_key].add_jvalue( str_val, line_num )
                    case "datetime":
                        self[json_key].add_jvalue( value, line_num )
                    case "int":
                        self[json_key].add_jvalue( value, line_num )
                    case "float":
                        self[json_key].add_jvalue( value, line_num )
                    case "str":
                        self[json_key].add_jvalue( value, line_num )
                    case "bool":
                        self[json_key].add_jvalue( value, line_num )
                    case _:
                        print(f"[KeyGraphBase.process_field ({log_key}:{json_key}={value})] type: {type(value)} unhandeled valuetype" )

                result = True

            except Exception as valexc:
                print( f"[KeyGraphBase.process_field ({log_key}:{json_key}={value})] type: {type(value)} ValueError: {valexc}" )

        else:
            if log_key not in self.missing_keys:
                self.missing_keys.append( log_key )

        return result

    def dump_key_groups( self: Self ) -> None:
        try:
            data_str = json.dumps( self.missing_keys, indent=4 )
            file_path = os.path.join( self._root_dir, "missedkeys.json" )
            open( file_path, "w" ).write( data_str )

            data_str = json.dumps( self.none_values, indent=4 )
            file_path = os.path.join( self._root_dir, "none_values.json" )
            open( file_path, "w" ).write( data_str )

            #data_str = json.dumps( self.message_fields, indent=4 )
            #file_path = os.path.join( self._root_dir, "message_fields.json" )
            #open( file_path, "w" ).write( data_str )

        except Exception as exc:
            print(f'KeyGraphBase.dump_key_groups: Exception: {exc}')







