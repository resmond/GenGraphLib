from enum import IntEnum
from typing import Self

import asyncio as aio

from src.gengraphlib import KeyValTypes, KeyFilter, KeyGroup, KeyDefBase

class SerializationType( IntEnum ):
    CSV = 1
    JArray = 2
    JObject = 3

class VectorValue:

    def __init__( self: Self, key_def: KeyDefBase, _alias: str | None = None ) -> None:
        super().__init__()
        self.key_def: KeyDefBase = key_def
        if _alias is None:
            self.field_name: str = self.key_def.json_key
        else:
            self.field_name: str = _alias

class GraphVector( dict[str, VectorValue ] ):

    def __init__( self, _key_group: KeyGroup, _key_filter: KeyFilter ):
        super().__init__()
        self._key_group: KeyGroup = _key_group
        self._filter_map: KeyFilter = _key_filter

        for json_key, key_def in self._key_group.items():
            if key_def.json_key in self._filter_map:
                if self._filter_map[key_def.json_key ] is not None:
                    self.add( key_def, self._filter_map[key_def.json_key ] )
            else:
                self.add( key_def )

    def add( self: Self, key_def: KeyDefBase, alias: str | None = None ):
        self.append( VectorValue( key_def, alias ) )

    def get_headers( self ) -> list[str]:
        return [field.field_name for field in self.values()]

    def write_text( self, keyval_source: dict[str, KeyValTypes], text_writer: aio.StreamWriter, format_type: SerializationType ):

        if format_type == SerializationType.JObject:
            list_of_values: list[bytes] = [b'{']
            back_token: bytes = b'}\n'
        else:
            list_of_values: list[bytes] = []
            back_token: bytes = b'\n'

        for key, vector_value in self.items():
            match format_type:
                case SerializationType.CSV:
                    pass

                case SerializationType.JArray:
                    pass

                case SerializationType.JObject:
                    next_value = keyval_source[ key ]
                    pass


            #slice_field.key_def.key_values



        list_of_values.append( back_token )
        text_writer.write( b",".join( list_of_values ) )






