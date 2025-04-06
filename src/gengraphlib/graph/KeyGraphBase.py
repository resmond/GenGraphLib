from typing import Self, Any

import json
import os

from .GraphKeys import (
    KeyDefBase,
    KeyGroups,
    DefaultDictOfLists,
    KeyValTypes,
)

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
        self.none_values: DefaultDictOfLists = DefaultDictOfLists()
        #self.message_fields: DefaultDictOfLists = DefaultDictOfLists()

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
        
    def process_fields( self, fields: dict[str,KeyValTypes], line_num: int, log_line: str = "" ) -> bool:

        for log_key, value in fields.items():
            self.process_field( log_key, value, line_num, log_line )

        return True

    def process_field( self: Self, log_key: str, value: Any, line_num: int, log_line: str = "" ) -> bool:

        json_key = self._log_keys[log_key].json_key

        if value is None:
            self.none_values.add_entry( log_key, log_line )
        elif log_key == "MESSAGE":
            log_str = f"[{value}]"
            self.message_fields.add_entry( log_key, log_str )

        if log_key in self._log_keys:
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
                result = False
                
        else:
            if log_key not in self.missing_keys:
                self.missing_keys.append( log_key )

            result = False

        return result

    def dump_key_values( self: Self ) -> None:

        key: str = ""
        try:
            for key, values_set in self.items():
                key_dir: str = os.path.join(self._root_dir, "keys", f"{key}")

                if not os.path.exists(key_dir):
                    os.mkdir(key_dir)

                with open(f'{key_dir}/{key}.json', "w") as keyfile:
                    for value_line in values_set:
                        value_line_json = json.dumps(value_line, indent=4)
                        keyfile.write(value_line_json)
                        keyfile.write("\n")

        except Exception as exc:
            print(f'[KeyGraphBase.dump_key_values] ({key})  Exception: {exc}')

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







