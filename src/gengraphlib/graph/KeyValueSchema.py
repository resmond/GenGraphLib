from typing import Self
from collections.abc import Iterable

import json
import os

from progress.bar import Bar

from .. import (
    KeyValTypes,
    keygroup_rec,
    KeyDefDict
)

from . import (
    StrKeyDef,
    IntKeyDef,
    BoolKeyDef,
    FloatKeyDef,
    TmstKeyDef,
    KeySchemaVisitor,
)

from . import (
    RecordBase,
    KeyDefBase,
    KeyGroups,
    GraphRecordRoot
)

class KeyValueSchema( dict[str, KeyDefBase ], GraphRecordRoot ):
    schema: Self

    def __init__( self: Self, id: str,  root_dir: str ) -> None:
        super( KeyValueSchema, self ).__init__()
        self.id = id
        self._root_dir = root_dir

        self._log_keys: KeyDefDict = KeyDefDict()
        self.missing_keys: list[str] = []
        self.none_values:  list[str] = []
        self.key_groups: KeyGroups = KeyGroups("key_groups",self)

        KeyValueSchema.schema = self

    def add_keydef( self: Self, _key_def: KeyDefBase ) -> None:
        self[_key_def.key ]             = _key_def
        self._log_keys[_key_def.alias ] = _key_def

    def add_keydefs( self: Self, _keydefs: list[KeyDefBase ] ) -> None:
        for _key_def in _keydefs:
            self.add_keydef(_key_def)

    def add_key_to_group( self: Self, _group_id: str | list[str], _key: str ) -> None:
        if isinstance(_group_id, str):
            if _group_id == "":
                _group_id = "skip"
            key_group = self.key_groups[_group_id ]
            key_def: KeyDefBase = self[_key]
            key_group.add_keydef(key_def)
        else:
            for id in _group_id:
                self.add_key_to_group(id, _key)

    def new_keygroup( self: Self, _group_id: str, _group_name: str = "", _group_desc: str = "", _keys: list[str] | None = None ) -> None:
        self.key_groups.add_keygroup( _group_id, _group_name, _group_desc )
        if _keys is not None:
            for _key in _keys:
                self.add_key_to_group( _group_id, _key )

    # noinspection PyTypeHints
    def define_keygroups( self: Self, recs: Iterable[keygroup_rec] ) -> None:
        self.key_groups.define_keygroups( recs )

    def init_repository( self ):
        for key, keydef in self.items():
            match keydef.groupids:
                case str():
                    self.add_key_to_group( keydef.groupids, key )
                case list():
                    for group_id in keydef.groupids:
                        self.add_key_to_group(group_id, key)

        self.final_init()

    def final_init( self ):
        pass

    @property
    def graph_id(self: Self) -> str:
        return self.id

    def add_record( self: Self, graph_rec: RecordBase ) -> None:
        pass

    def apply_values( self: Self, graph_rec: RecordBase, _log_key: str, value: str ) -> None:
        pass

    def get_typed_keydef[T: KeyValTypes]( self, key: str ) -> KeyDefBase[T] | None:
        if key in self:
            key_def: KeyDefBase = self[key]
            if isinstance(key_def, KeyDefBase):
                return key_def
        return None

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
            print(f'[KeySchemaBase.read_json]FileNotFoundError: {ext} - {filepath}')

    def persist_data( self: Self ):
        self._persist_keys()
        self._log_traces()

    # noinspection PyUnresolvedReferences
    def _persist_keys( self: Self, source_id: str = "all", line_numbers: bool = False ) -> None:

        key: str = ""
        try:
            keydef: KeyDefBase
            for key, keydef in self.items():
                key_dir: str = os.path.join(self._root_dir, "keys", f"{key}")

                if not os.path.exists(key_dir):
                    os.mkdir(key_dir)

                with open(f'{key_dir}/{source_id}-{key}.jline', "w") as keyfile:
                    for value, lines in keydef.key_values.items():
                        if line_numbers:
                            lines_json = json.dumps(lines)
                            keyfile.write(f'{value}')
                            keyfile.write(f'    {lines_json}')
                        else:
                            keyfile.write(f'[{len(lines):5}]: {value}\n')

        except Exception as exc:
            print(f'[KeySchemaBase.dump_key_values] ({key})  Exception: {exc}')

    def _log_traces( self: Self ) -> None:
        try:
            data_str = json.dumps( self.missing_keys, indent=4 )
            file_path = os.path.join( self._root_dir, "missedkeys.json" )
            open( file_path, "w" ).write( data_str )

            data_str = json.dumps( self.none_values, indent=4 )
            file_path = os.path.join( self._root_dir, "none_values.json" )
            open( file_path, "w" ).write( data_str )

        except Exception as exc:
            print(f'KeySchemaBase.dump_key_groups: Exception: {exc}')

    #from src.gengraphlib.graph.KeyValVisitorBase import KeyValueVisitorBase
    def visit_schema[ T: KeySchemaVisitor ]( self: Self, visitor: T ) -> bool:
        for key, key_def in self.items():
            #from src.gengraphlib.graph.KeyDefs import FloatKeyDef
            match key_def:
                case StrKeyDef():
                    visitor.visit_str( key_def, key_def.key_values )
                case IntKeyDef():
                    visitor.visit_int( key_def, key_def.key_values )
                case FloatKeyDef():
                    visitor.visit_float( key_def, key_def.key_values )
                case BoolKeyDef():
                    visitor.visit_bool( key_def, key_def.key_values )
                case TmstKeyDef():
                    visitor.visit_tmst( key_def, key_def.key_values )
                case _:
                    pass
        return True


