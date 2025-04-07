from collections.abc import Iterable
from typing import Self

from KeyDefs import KeyDefBase

keygroup_rec = tuple[str, str, str | None, list[str] | None]

class KeyGroup( list[KeyDefBase] ):
    def __init__( self: Self, group_id: str, group_name: str = None, group_desc: str = "" ) -> None:
        self.group_id: str = group_id
        self.group_name: str = group_name or group_id
        self.group_desc: str = group_desc
        super( KeyGroup, self ).__init__()

    def add_keydef(self: Self, other: KeyDefBase) -> None:
        self.append(other)

class KeyGroups( dict[str, KeyGroup ] ):
    def __init__( self: Self, graph_root: dict[str,KeyDefBase ] ) -> None:
        super(KeyGroups, self).__init__()
        self.graph_root: dict[str,KeyDefBase ] = graph_root

    def add_keygroup( self: Self, group_id: str, group_name: str = "", group_desc = "" ) -> None:
        self[group_id ] = KeyGroup( group_id, group_name, group_desc )

    def def_keygroup( self: Self, _keygroup_rec: keygroup_rec ):
        self.add_keygroup( _keygroup_rec[0], _keygroup_rec[1], _keygroup_rec[2] )
        #self.add_keys_to_group( _keygroup_rec[0], _keygroup_rec[3] )

    def add_key_to_group( self: Self, _group_id: str, _key_def: KeyDefBase ) -> None:
        key_group: KeyGroup = self[_group_id ]
        key_group.add_keydef(_key_def)

    def add_keys_to_group( self: Self, _keygroup_name: str, keys: Iterable[str]) -> None:
        for _json_key in keys:
            _key_def = self.graph_root[_json_key]
            self.add_key_to_group( _keygroup_name, _key_def )

    def define_keygroups( self: Self, recs: Iterable[keygroup_rec] ) -> None:
        for rec in recs:
            group_id: str = rec[0]
            group_name: str = rec[1] or group_id
            group_desc: str = rec[2] or ""
            self.def_keygroup( (group_id, group_name, group_desc, None) )

            if len(rec) == 4:
                self.add_keys_to_group( group_id, rec[3] )
