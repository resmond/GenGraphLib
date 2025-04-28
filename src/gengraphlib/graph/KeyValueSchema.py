from typing import Self
from collections.abc import Iterable

import json
import os

from ..common import KeyValTypes, keygroup_rec, KeyDefDict, KeyInfo, KeyValSchemaInfo

from .GraphLib import GraphRecordRoot
from .KeyDefs import KeyDefBase, StrKeyDef, IntKeyDef, BoolKeyDef, FloatKeyDef, TmstKeyDef
from .KeyGroups import KeyGroups
from .KeySchemaVisitor import KeySchemaVisitor

class KeyValueSchema( dict[str, KeyDefBase ], GraphRecordRoot ):

    def __init__( self: Self, id: str,  root_dir: str ) -> None:
        super( KeyValueSchema, self ).__init__()
        self.id = id
        self._root_dir = root_dir
        self._alias_map: KeyDefDict = KeyDefDict()
        self.key_groups: KeyGroups = KeyGroups("key_groups",self)
        self.schema_info: KeyValSchemaInfo | None = None
        self.missing_keys: list[str] = []
        self.none_values:  list[str] = []

    @property
    def graph_id(self: Self) -> str:
        return self.id

    def add_keydef( self: Self, _key_def: KeyDefBase ) -> None:
        self[_key_def.key ]             = _key_def
        self._alias_map[_key_def.alias ] = _key_def

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

        self.schema_info = self.get_schema_info()

    def get_schema_info( self: Self ) -> KeyValSchemaInfo:
        keys: list[KeyInfo] = [ key.get_keyinfo() for key in self.values() ]
        groupids: list[str] = [ group.id for group in self.key_groups.values() ]
        return KeyValSchemaInfo( keys, groupids )

    def get_groupkeys( self, group_id: str ) -> set[str ]:
        return { keydef.alias for key, keydef in self.items() if keydef.in_group(group_id) }

    # noinspection PyTypeChecker
    def by_alias( self: Self, alias: str ) -> KeyDefBase:
        return self._alias_map[alias ]

    def get_typed_keydef[T: KeyValTypes]( self, key: str ) -> KeyDefBase[T] | None:
        if key in self:
            key_def: KeyDefBase = self[key]
            if isinstance(key_def, KeyDefBase):
                return key_def
        return None

    def log_traces( self: Self ) -> None:
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
                    visitor.visit_str( key_def )
                case IntKeyDef():
                    visitor.visit_int( key_def )
                case FloatKeyDef():
                    visitor.visit_float( key_def )
                case BoolKeyDef():
                    visitor.visit_bool( key_def )
                case TmstKeyDef():
                    visitor.visit_tmst( key_def )
                case _:
                    pass
        return True


