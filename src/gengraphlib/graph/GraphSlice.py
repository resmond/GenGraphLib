from enum import IntEnum
from typing import Self

from sphinx.writers.text import TextWriter

from .KeyGroups import KeyGroup
from .KeyDefs import KeyDefBase
from .. import KeyValTypes


class SliceFormatType(IntEnum):
    CSV = 1
    JArray = 2
    JObject = 3

class GraphSliceField:

    def __init__( self: Self, key_def: KeyDefBase, _alias: str | None = None ) -> None:
        super().__init__()
        self.key_def: KeyDefBase = key_def
        self.field_name: str = _alias or key_def.json_key

class GraphSliceDef( dict[str, GraphSliceField] ):

    def __init__( self, _key_group: KeyGroup, _aliases: dict[str, str | None ] = [] ):
        super().__init__()
        self._key_group: KeyGroup = _key_group
        self._aliases: dict[str, str] | None = _aliases

        for key_def in self._key_group:
            if key_def.json_key in self._aliases:
                if self._aliases[key_def.json_key] is not None:
                    self.add( key_def, self._aliases[key_def.json_key] )
            else:
                self.add( key_def )

    def add( self: Self, key_def: KeyDefBase, alias: str | None = None ):
        self.append( GraphSliceField( key_def ) )

    def get_headers( self ) -> list[str]:
        header_namelist: list[str] = []
        for key, slice_field in self.items():
            header_namelist.append( slice_field.field_name )
        return header_namelist

    def write_slice( self, keyval_source: dict[str, KeyValTypes], file_handle: TextWriter, format_type: SliceFormatType ):
        list_of_values: list[str] = []
        for key, slice_field in self.items():
            pass

        match format_type:
            case SliceFormatType.CSV:
                file_handle.write( ",".join( list_of_values ) )
                file_handle.write( "\n" )










