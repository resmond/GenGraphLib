from collections.abc import Iterable
from typing import Self

from src.gengraphlib.common import (
    KeyGroupRec,
    KeyDefDict,
    KeyDefInterface,
    KeyDefRoot
)

from src.gengraphlib.graphs.GraphLib import (
    GNodeInterface,
)

class KeyGroup( KeyDefDict, GNodeInterface ):
    def __init__( self: Self, id: str, group_desc: str = "" ) -> None:
        super().__init__()
        self.id: str = id
        self.group_desc: str = group_desc

    def add_keydef( self: Self, key_def: KeyDefInterface ) -> None:
        self[ key_def.key ] = key_def

class KeyGroups( dict[str, KeyGroup ], GNodeInterface ):
    def __init__( self: Self, id: str, graph_root: KeyDefRoot ) -> None:
        super().__init__()
        self.id: str = id
        self.graph_root: KeyDefRoot = graph_root

    def add_keygroup( self: Self, group_id: str, group_desc: str = "", keys: Iterable[str] | None = None ) -> None:
        self[group_id] = KeyGroup( group_id, group_desc )
        if keys is not None:
            self.add_keys_to_group( group_id, keys )

    def def_keygroup( self: Self, _keygroup_rec: KeyGroupRec ):
        group_id: str = _keygroup_rec[0]
        group_desc: str = ""
        keys: Iterable[str] | None = None

        match len(_keygroup_rec):
            case 1:
                pass
            case 2 if isinstance( _keygroup_rec[1], str ):
                group_desc = _keygroup_rec[1]
            case 2 if isinstance( _keygroup_rec[1], Iterable ):
                keys = _keygroup_rec[1]
            case 3:
                group_desc = _keygroup_rec[1]
                keys = _keygroup_rec[2]
            case _:
                return

        self.add_keygroup( group_id, group_desc, keys )

    def add_key_to_group( self: Self, _group_id: str, _key_def: KeyDefInterface ) -> None:
        key_group: KeyGroup = self[_group_id ]
        key_group.add_keydef(_key_def)

    def add_keys_to_group( self: Self, _keygroup_id: str, keys: Iterable[str] ) -> None:
        for _json_key in keys:
            _key_def = self.graph_root[_json_key]
            self.add_key_to_group( _keygroup_id, _key_def )

    # noinspection PyTypeHints
    def define_keygroups( self: Self, recs: Iterable[KeyGroupRec] ) -> None:
        for rec in recs:
            self.def_keygroup( rec )
