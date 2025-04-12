from collections.abc import Iterable
from typing import Self

from .. import KeyFilter
from .GraphVector import GraphVector
from .KeyDefs import KeyDefBase

KeyGroupRec = tuple[str] |tuple[str, str] | tuple[str, str, Iterable[str]]

class KeyGroup( dict[str, KeyDefBase ] ):
    def __init__( self: Self, group_id: str, group_desc: str = "" ) -> None:
        super().__init__()
        self.group_id: str = group_id
        self.group_desc: str = group_desc

    def add_keydef( self: Self, key_def: KeyDefBase ) -> None:
        self[ key_def.json_key ]( key_def )

    def create_slice( self: Self, _key_filter: KeyFilter ) -> GraphVector:
        return GraphVector( self, _key_filter )

class KeyGroups( dict[str, KeyGroup ] ):
    def __init__( self: Self, graph_root: dict[str,KeyDefBase ] ) -> None:
        super().__init__()
        self.graph_root: dict[str,KeyDefBase ] = graph_root

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

    def add_key_to_group( self: Self, _group_id: str, _key_def: KeyDefBase ) -> None:
        key_group: KeyGroup = self[_group_id ]
        key_group.add_keydef(_key_def)

    def add_keys_to_group( self: Self, _keygroup_id: str, keys: Iterable[str] ) -> None:
        for _json_key in keys:
            _key_def = self.graph_root[_json_key]
            self.add_key_to_group( _keygroup_id, _key_def )

    def define_keygroups( self: Self, recs: Iterable[KeyGroupRec] ) -> None:
        for rec in recs:
            self.def_keygroup( rec )
