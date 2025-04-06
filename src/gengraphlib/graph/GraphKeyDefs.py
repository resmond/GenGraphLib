from typing import Self

import datetime as dt
import json
import os

from abc import abstractmethod, ABC
from enum import IntEnum
from collections.abc import Callable
from sortedcontainers import SortedDict

KeyValTypes: type = type[str, int, bool, dt.datetime]

process_fields_fn = Callable[ [ dict[str,KeyValTypes], int, str | None], int ]

class KeyType( IntEnum ):
    KStr         = 1
    KInt         = 2
    KBool        = 3
    KTimeStamp  = 4

class LineRefList( list[ int ] ):
    pass

class KeyValueInstancesBase[ T: KeyValTypes ]( SortedDict[ T, LineRefList ] ):
    def __init__(self: Self) -> None:
        super().__init__()
        self.unique: bool = True

    def add_value( self: Self, new_value: T, line_num: int ) -> None:
        if new_value not in self:
            self[new_value] = LineRefList()
        else:
            self.unique = False

        self[new_value].append( line_num )

    def __repr__( self: Self ) -> str:
        return f'{{unique:{self.unique}, cnt:{len(self)}'

class KeyDefBase[ T: KeyValTypes]( ABC ):
    def __init__( self: Self, _json_key: str, _log_key: str, _key_type: KeyType, groups: list[str] | str | None = None) -> None:
        super(KeyDefBase, self).__init__()
        self.json_key: str = _json_key
        self.log_key: str = _log_key
        self.key_type: KeyType = _key_type
        self.groups: list[str] | None = None
        self.skip: bool = False
        self.key_values: KeyValueInstancesBase[T] = KeyValueInstancesBase[T]()

        if groups is str:
            if groups == "skip":
                self.skip = True
            self.groups = [groups]
        if groups is not None:
            self.groups: list[str] = groups
            if "skip" in self.groups:
                self.skip = True
        else:
            self.groups = None

    def add_value( self: Self, new_value: T, line_num: int ) -> None:
        self.key_values.add_value(new_value, line_num)

    @abstractmethod
    def add_jvalue( self: Self, jvalue: KeyValTypes, line_num: int ) -> None:
        pass

class StrKeyDef( KeyDefBase[str] ):
    def __init__( self, _json_key: str, _log_key: str, groups: list[str] | str | None = None ):
        super( StrKeyDef, self ).__init__( _json_key, _log_key, KeyType.KStr, groups )

    def add_jvalue( self: Self, jvalue: str, line_num: int ) -> None:
        self.key_values.add_value( jvalue, line_num )

class IntKeyDef( KeyDefBase[int] ):
    def __init__( self, _json_key: str, _log_key: str, groups: list[str] | str  | None = None ):
        super( IntKeyDef, self ).__init__( _json_key, _log_key, KeyType.KInt, groups )

    def add_jvalue( self: Self, jvalue: str, line_num: int ) -> None:
        self.key_values.add_value( int( jvalue ), line_num )

class BoolKeyDef( KeyDefBase[bool] ):
    def __init__( self, _json_key: str, _log_key: str, groups: list[str] | str  | None = None ):
        super( BoolKeyDef, self ).__init__( _json_key, _log_key, KeyType.KBool, groups )

    def add_jvalue( self: Self, jvalue: str, line_num: int ) -> None:
        self.key_values.add_value( bool( jvalue ), line_num )

class TmstKeyDef( KeyDefBase[dt.datetime ] ):
    def __init__( self, _json_key: str, _log_key: str, groups: list[str] | str  | None = None ):
        super( TmstKeyDef, self ).__init__( _json_key, _log_key, KeyType.KTimeStamp, groups )

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

class KeyDefIndex( dict[str, KeyDefBase ] ):
    def __init__( self: Self ) -> None:
        super(KeyDefIndex, self).__init__()

class KeyRepository( dict[str, KeyDefBase ], ABC ):
    def __init__( self: Self, root_dir: str ) -> None:
        super(KeyRepository, self).__init__()
        self._root_dir = root_dir
        self.key_groups: KeyGroups = KeyGroups(self)

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

    def init_repository( self ):
        for key, keydef in self.items():
            if keydef.groups is not None:
                for group_id in keydef.groups:
                    self.add_key_to_group( group_id, key )

    def process_fields( self, fields: dict[str,KeyValTypes], line_num: int, log_line: str = "" ) -> bool:

        for log_key, value in fields.items():
            self.process_field( log_key, value, line_num, log_line )

        return True

    @abstractmethod
    def process_field( self: Self, log_key: str, value: KeyValTypes, line_num: int, log_line: str = "" ) -> bool:
        pass

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


