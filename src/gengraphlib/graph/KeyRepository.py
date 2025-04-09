from typing import Self, Any
from collections.abc import Iterable
from abc import abstractmethod

import json
import os

from .KeyDefs import (
    KeyDefBase,
    KeyValTypes,
    StrKeyDef,
    IntKeyDef,
    BoolKeyDef,
    TmstKeyDef
)

from .KeyProps import KeyPropRepository, KeyPropBase
from .KeyGroups import KeyGroups, keygroup_rec
from .KeyProps import StrKeyProp
from .KeyValues import AddValueResult, KeyValueTriggerBase

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

class KeyRepository( dict[str, KeyDefBase], KeyPropRepository ):
    def __init__( self: Self, root_dir: str ) -> None:
        self._root_dir = root_dir
        self.key_groups: KeyGroups = KeyGroups(self)
        self.none_values: DefaultDictOfLists = DefaultDictOfLists()
        self.missing_keys: list[str] = []
        super().__init__()
        #super(KeyPropRepository, self).__init__()

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

    @abstractmethod
    def final_init( self ):
        self.keyprops_init()
        pass

    def get_typed_keydef[T: KeyValTypes]( self, key: str ) -> KeyDefBase[T] | None:
        if self.__contains__( key ):
            key_def: KeyDefBase = self[key]
            match type(key_def):
                case StrKeyDef():
                    return key_def
                case IntKeyDef():
                    return key_def
                case BoolKeyDef():
                    return key_def
                case TmstKeyDef():
                    return key_def
                case _:
                    return None

        return None

    def get_typed_keyprop[T: KeyValTypes]( self, key: str ) -> KeyPropBase[T] | None:
        if self.keyprops_list.__contains__( key ):
            key_def: KeyDefBase = self[key]

            if isinstance(key_def, KeyPropBase):
                key_prop: KeyPropBase = key_def
                match type(key_prop):
                    case StrKeyProp():
                        return key_def
                    case _:
                        return None

        return None

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
                val_result: AddValueResult | None = None
                match type(value).__name__:
                    case "list":
                        str_val = str(value)
                        val_result = self[json_key].add_jvalue( str_val, line_num )
                    case "datetime":
                        val_result = self[json_key].add_jvalue( value, line_num )
                    case "int":
                        val_result = self[json_key].add_jvalue( value, line_num )
                    case "float":
                        val_result = self[json_key].add_jvalue( value, line_num )
                    case "str":
                        val_result = self[json_key].add_jvalue( value, line_num )
                    case "bool":
                        val_result = self[json_key].add_jvalue( value, line_num )
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

"""
{"_SYSTEMD_INVOCATION_ID":"624f1d96f4894cc5929f65e6fa587096"
_CMDLINE":"/usr/lib/systemd/systemd-modules-load"
_CAP_EFFECTIVE":"1ffffffffff"
PRIORITY":"6"

__REALTIME_TIMESTAMP":"1744028103096482"
_SOURCE_REALTIME_TIMESTAMP":"1744028103064722"

_TRANSPORT":"journal"
_COMM":"systemd-modules"
_UID":"0"
_MACHINE_ID":"4395b976dd294dd58d7b1ecc1f066791"
_BOOT_ID":"4ffdd8ebe9c24b5c8e62570b49a5e223"
__SEQNUM":"7382494"
CODE_FUNC":"module_load_and_warn"
_SYSTEMD_SLICE":"system.slice"
SYSLOG_FACILITY":"3"
_SELINUX_CONTEXT":"unconfined\n"
SYSLOG_IDENTIFIER":"systemd-modules-load"
_RUNTIME_SCOPE":"system"
_EXE":"/usr/lib/systemd/systemd-modules-load"
MESSAGE":"Inserted module 'lp'","CODE_LINE":"137"
CODE_FILE":"src/shared/module-util.c"
TID":"553"
__MONOTONIC_TIMESTAMP":"3874654"
__SEQNUM_ID":"7d0971a098e24097a784ffa07ef8d85f"
_SYSTEMD_CGROUP":"/system.slice/systemd-modules-load.service"
_SYSTEMD_UNIT":"systemd-modules-load.service"
_GID":"0"
_HOSTNAME":"gernby-NUC13ANHi7","_PID":"553"
__CURSOR":"s=7d0971a098e24097a784ffa07ef8d85f;i=70a5de;b=4ffdd8ebe9c24b5c8e62570b49a5e223;m=3b1f5e;t=6322f2f9038a2;x=6049ddda03b4ddb4"}
"""