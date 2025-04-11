from typing import Self, Protocol
from collections.abc import Iterable
from abc import abstractmethod

import json
import os

from progress.bar import Bar

#from src.gengraphlib import KeyPropBase, KeyDefBase
from .KeyDefs import (
    KeyDefBase,
    KeyValTypes
)

from .KeyProps import KeyPropBase
from .KeyGroups import KeyGroups
from .KeyValues import AddValueResult, KeyValueTriggerBase
from .. import keygroup_rec


class FieldProcessor(Protocol):
    def process_keyvalues( self: Self, fields: dict[str,KeyValTypes ], line_num: int, log_line: str ) -> bool:
        pass


"""
    DefaultDictOfLists
"""
class DefaultDictOfLists(dict[str, list[str]]):

    def __init__( self: Self ) -> None:
        super().__init__()

    def add_entry( self: Self, key: str, value: str ) -> None:
        if key not in self:
            self[key] = []
        self[key].append( value )

class KeyDefIndex( dict[str, KeyDefBase ] ):
    def __init__( self: Self ) -> None:
        super().__init__()

class KeyGraphBase( dict[str, KeyDefBase ], FieldProcessor ):
    def __init__( self: Self, root_dir: str ) -> None:
        super().__init__()
        self._root_dir = root_dir
        self.key_groups: KeyGroups = KeyGroups(self)
        self.none_values: DefaultDictOfLists = DefaultDictOfLists()
        self.missing_keys: list[str] = []

    def __init_subclass__( cls ):
        super().__init_subclass__()

    def add_keydef( self: Self, _key_def: KeyDefBase ) -> None:
        self[_key_def.json_key] = _key_def
        self._log_keys[_key_def.log_key] = _key_def

    def add_keydefs( self: Self, _keydefs: list[KeyDefBase ] ) -> None:
        for _key_def in _keydefs:
            self.add_keydef(_key_def)

    def add_key_to_group( self: Self, _group_id: str, _key: str ) -> None:
        if _group_id == "":
            _group_id = "skip"
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

        self.final_init()

    def final_init( self ):
        #self.keyprops_init()
        pass

    def get_typed_keydef[T: KeyValTypes]( self, key: str ) -> KeyDefBase[T] | None:
        if key in self:
            key_def: KeyDefBase = self[key]
            if isinstance(key_def, KeyDefBase):
                return key_def
        return None

    def get_typed_keyprop[T: KeyValTypes]( self, key: str ) -> KeyPropBase[T]  | None:
        if key in self:
            key_def: KeyDefBase = self[key]
            if isinstance(key_def, KeyPropBase):
                return key_def

        return None

    def process_keyvalues( self, fields: dict[str,KeyValTypes ], line_num: int, log_line: str ) -> bool:

        for log_key, value in fields.items():
            self.process_field( log_key, value, line_num, log_line )

        return True

    def process_field( self: Self, key: str, value: KeyValTypes, rec_num: int, rec_line: str = "" ) -> bool:
        key_def: KeyDefBase | None = self.get(key, None)
        if key_def is not None:
            return self.process_keyvalue( key_def, value, rec_num, rec_line )
        else:
            return False

    def process_keyvalue( self, key_def: KeyDefBase, value: KeyValTypes, rec_num: int, rec_line: str = "" ) -> bool:

        result: bool = False

        json_key = key_def.json_key

        if value is None:
            self.none_values.add_entry( json_key, rec_line )

        elif key_def.dologing:
            try:
                val_result: AddValueResult | None = None
                match type(value).__name__:
                    case "str":
                        val_result = self[json_key].add_jvalue( value, rec_num )
                    case "datetime":
                        val_result = self[json_key].add_jvalue( value, rec_num )
                    case "int":
                        val_result = self[json_key].add_jvalue( value, rec_num )
                    case "bool":
                        val_result = self[json_key].add_jvalue( value, rec_num )
                    case "float":
                        val_result = self[json_key].add_jvalue( value, rec_num )
                    case "list":
                        str_val = str(value)
                        val_result = self[json_key].add_jvalue( str_val, rec_num )
                    case _:
                        print(f"[KeyGraphBase.process_field ({json_key}:{json_key}={value})] type: {type( value )} unhandeled valuetype" )

                if val_result is not None:
                    self.keyvalue_trigger( val_result )

                result = True

            except Exception as valexc:
                print( f"[KeyGraphBase.process_field ({json_key}:{json_key}={value})] type: {type( value )} ValueError: {valexc}" )

        else:
            if json_key not in self.missing_keys:
                self.missing_keys.append( json_key )

        return result

    @abstractmethod
    def keyvalue_trigger( self: Self, val_result: KeyValueTriggerBase ) -> AddValueResult:
        print(f"[Trigger]: {val_result}")
        return val_result

    def read_json(self: Self, filepath: str):
        try:
            line_num: int = 0
            read_len: int = 0
            file_size: int = os.path.getsize(filepath)
            bar = Bar("Processing", max=file_size)
            with open(filepath) as file:
                for line in file:
                    read_len += len(line)
                    field_dict = json.loads(line)
                    self.process_keyvalues( field_dict, line_num, line )
                    bar.next(read_len )
            bar.finish()
        except FileNotFoundError as ext:
            print(f'[JsonLogKeyGraph.read_json]FileNotFoundError: {ext} - {filepath}')


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

