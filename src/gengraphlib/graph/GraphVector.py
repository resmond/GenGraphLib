from typing import Self

import asyncio as aio

from .. import SerializationType, KeyFilter
from .  import KeyDefBase, KeyDefDict

class VectorValue:

    def __init__( self: Self, key_def: KeyDefBase, _alias: str | None = None ) -> None:
        super().__init__()
        self.key_def: KeyDefBase = key_def
        if _alias is None:
            self.field_name: str = self.key_def.json_key
        else:
            self.field_name: str = _alias

class GraphVector( dict[str, VectorValue ] ):
    def __init__( self, _key_group: KeyDefDict  , _key_filter: KeyFilter ):
        super().__init__()

        self._key_group: KeyDefDict = _key_group
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
        return [vector_value.field_name for vector_value in self.values()]

    def write_all( self, binary_writer: aio.StreamWriter, format_type: SerializationType ) -> bool:

        if format_type == SerializationType.JObject:
            list_of_values: list[bytes] = [b'{']
            back_token: bytes = b'}\n'
        else:
            list_of_values: list[bytes] = []
            back_token: bytes = b'\n'

        first = True
        data_str: str = ""

        for key, vector_value in self.items():
            match format_type:
                case SerializationType.CSV:
                    data_str = f"{str(vector_value)}"
                    pass

                case SerializationType.JArray:
                    data_str = f"'{str(vector_value)}'"
                    pass

                case SerializationType.JObject:
                    data_str = f"'{key}':'{str(vector_value)}'"
                    #next_value = keyval_source[ key ]
                    pass

            if not first:
                bin_data = ",{data_str}".encode()
            else:
                bin_data = data_str.encode()

            list_of_values.append( bin_data )
            first = False

        list_of_values.append( back_token )

        try:
            formatted_headers: list[str] = [f' {header:10} ' for header in self.get_headers()]
            headers_line: str = "".join( formatted_headers )
            binary_writer.write( headers_line.encode() )
            binary_writer.write( b",".join( list_of_values ) )

        except Exception as exc:
            print(f"GraphVector.write_text: {exc}")
            return False

        return True

class GraphValueResult:

    def __init__( self: Self, key_def: KeyDefBase, value: str | None = None ):
        super().__init__()
        self.key_def: KeyDefBase = key_def
        self.value: str = value



