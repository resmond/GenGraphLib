from enum import IntEnum
from typing import Self

import asyncio as aio

from .. import KeyValTypes, KeyFilter
from .KeyGroups import KeyGroup
from .KeyDefs import KeyDefBase


class SliceFormatType(IntEnum):
    CSV = 1
    JArray = 2
    JObject = 3

class GraphViewField:

    def __init__( self: Self, key_def: KeyDefBase, _alias: str | None = None ) -> None:
        super().__init__()
        self.key_def: KeyDefBase = key_def
        if _alias is None:
            self.field_name: str = self.key_def.json_key
        else:
            self.field_name: str = _alias

class GraphView( dict[str, GraphViewField ] ):

    def __init__( self, _key_group: KeyGroup, _key_filter: KeyFilter ):
        super().__init__()
        self._key_group: KeyGroup = _key_group
        self._filter_map: KeyFilter = _key_filter

        for key_def in self._key_group:
            if key_def.json_key in self._filter_map:
                if self._filter_map[key_def.json_key ] is not None:
                    self.add( key_def, self._filter_map[key_def.json_key ] )
            else:
                self.add( key_def )

    def add( self: Self, key_def: KeyDefBase, alias: str | None = None ):
        self.append( GraphViewField( key_def, alias ) )

    def get_headers( self ) -> list[str]:
        return [field.field_name for field in self.values()]

    def write_text( self, keyval_source: dict[str, KeyValTypes], text_writer: aio.StreamWriter, format_type: SliceFormatType ):
        list_of_values: list[bytes] = []
        for key, slice_field in self.items():
            #slice_field.key_def.key_values
            pass

        match format_type:
            case SliceFormatType.CSV:
                text_writer.write( b",".join( list_of_values ) )
                text_writer.write( b"\n" )









