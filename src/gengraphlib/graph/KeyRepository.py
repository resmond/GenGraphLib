from collections.abc import Iterable
from typing import Self, Any

import json
import os

from abc import ABC

from .KeyDefs import KeyDefBase, KeyValTypes
from .KeyGroups import KeyGroups, keygroup_rec

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

class KeyDefIndex( dict[str, KeyDefBase ] ):
    def __init__( self: Self ) -> None:
        super(KeyDefIndex, self).__init__()

class KeyRepository( dict[str, KeyDefBase ], ABC ):
    def __init__( self: Self, root_dir: str ) -> None:
        self._root_dir = root_dir
        self.key_groups: KeyGroups = KeyGroups(self)
        self.none_values: DefaultDictOfLists = DefaultDictOfLists()
        self.missing_keys: list[str] = []
        super(KeyRepository, self).__init__()

    def add_keydef( self: Self, _key_def: KeyDefBase ) -> None:
        self[_key_def.json_key] = _key_def
        self._log_keys[_key_def.log_key] = _key_def

    def add_keydefs( self: Self, _keydefs: list[KeyDefBase ] ) -> None:
        for _key_def in _keydefs:
            self.add_keydef(_key_def)

    def add_key_to_group( self: Self, _group_id: str, _key: str ) -> None:
        key_group = self.key_groups[_group_id ]
        key_def: KeyDefBase = self[_key]
        key_group.add_keydef(key_def)

    def new_keygroup( self: Self, _group_id: str, _group_name: str = "", _group_desc: str = "", _keys: list[str] | None = None ) -> None:
        self.key_groups.add_keygroup( _group_id, _group_name, _group_desc )
        if _keys is not None:
            for _key in _keys:
                self.add_key_to_group( _group_id, _key )

    def define_keygroups( self: Self, recs: Iterable[keygroup_rec] ) -> None:
        self.key_groups.define_keygroups( recs )

    def init_repository( self ):
        for key, keydef in self.items():
            match keydef.groups:
                case str():
                    self.add_key_to_group(keydef.groups, key)
                case list():
                    for group_id in keydef.groups:
                        self.add_key_to_group(group_id, key)

    def process_fields( self, fields: dict[str,KeyValTypes], line_num: int, log_line: str = "" ) -> bool:

        for log_key, value in fields.items():
            self.process_field( log_key, value, line_num, log_line )

        return True

    def process_field( self: Self, key: str, value: Any, line_num: int, log_line: str = "" ) -> bool:
        key_def: KeyDefBase | None = self.get(key, None)
        if key_def is not None:
            return self.process_keyvalue( key_def, value, line_num, log_line )
        else:
            return False

    def process_keyvalue( self, key_def: KeyDefBase, value: Any, line_num: int, log_line: str = "" ) -> bool:

        result: bool = False

        json_key = key_def.json_key

        if value is None:
            self.none_values.add_entry( json_key, log_line )

        elif key_def.dologing:
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
                        print(f"[KeyGraphBase.process_field ({json_key}:{json_key}={value})] type: {type( value )} unhandeled valuetype" )

                result = True

            except Exception as valexc:
                print( f"[KeyGraphBase.process_field ({json_key}:{json_key}={value})] type: {type( value )} ValueError: {valexc}" )

        else:
            if json_key not in self.missing_keys:
                self.missing_keys.append( json_key )

        return result

    def dump_key_values( self: Self, source_id: str = "all",  line_numbers: bool = False ) -> None:

        key: str = ""
        try:
            keydef: KeyDefBase
            for key, keydef in self.items():
                key_dir: str = os.path.join(self._root_dir, "keys", f"{key}")

                if not os.path.exists(key_dir):
                    os.mkdir(key_dir)

                with open(f'{key_dir}/{source_id}-{key}.txt', "w") as keyfile:
                    for value, lines in keydef.key_values.items():
                        if line_numbers:
                            lines_json = json.dumps(lines)
                            keyfile.write(f'{value}')
                            keyfile.write(f'    {lines_json}')
                        else:
                            keyfile.write(f'[{len(lines):5}]: {value}\n')

        except Exception as exc:
            print(f'[KeyGraphBase.dump_key_values] ({key})  Exception: {exc}')

    def dump_trace_groups( self: Self ) -> None:
        try:
            data_str = json.dumps( self.missing_keys, indent=4 )
            file_path = os.path.join( self._root_dir, "missedkeys.json" )
            open( file_path, "w" ).write( data_str )

            data_str = json.dumps( self.none_values, indent=4 )
            file_path = os.path.join( self._root_dir, "none_values.json" )
            open( file_path, "w" ).write( data_str )

        except Exception as exc:
            print(f'KeyGraphBase.dump_key_groups: Exception: {exc}')
