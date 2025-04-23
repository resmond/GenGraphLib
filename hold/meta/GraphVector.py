from typing import Self

import asyncio as aio

from .. import SerializationType, KeyFilter, KeyDefDict, KeyDefInterface

class VectorValue:

    def __init__( self: Self, key_def: KeyDefInterface, _alias: str | None = None ) -> None:
        super().__init__()
        self.key_def: KeyDefInterface = key_def
        if _alias is None:
            self.field_name: str = self.key_def.key
        else:
            self.field_name: str = _alias

class GraphVector( dict[str, VectorValue ] ):
    def __init__( self, _key_group: KeyDefDict  , _key_filter: KeyFilter ):
        super().__init__()

        self._key_group: KeyDefDict = _key_group
        self._filter_map: KeyFilter = _key_filter

        for json_key, key_def in self._key_group.items():
            if key_def.key in self._filter_map:
                if self._filter_map[key_def.key ] is not None:
                    self.add( key_def, self._filter_map[key_def.key ] )
            else:
                self.add( key_def )

    def add( self: Self, key_def: KeyDefInterface, alias: str | None = None ):
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

    def __init__( self: Self, key_def: KeyDefInterface, value: str | None = None ):
        super().__init__()
        self.key_def: KeyDefInterface = key_def
        self.value: str = value



# KeyValTypes: type = type[ str, int, bool, float, dt.datetime ]
#
# class KeyType( IntEnum ):
#     KStr    = 1
#     KInt    = 2
#     KBool   = 3
#     KFloat  = 4
#     KTmst   = 5
#
#
# @dataclass
# class KeyInfo:
#     schema_id: str
#     key: str
#     alias: str
#     keytype: KeyType
#     groupids: list[str] = field(default_factory=list)
#
#     @property
#     def keyinfo_id( self: Self ) -> str:
#         return f"{self.schema_id}@{self.key}"
#
# process_fields_fn = Callable[ [ dict[ str, KeyValTypes ], int, str], bool ]
#
# str_fn = Callable[ str, bytes ]
# int_fn = Callable[ int, bytes ]
# bool_fn = Callable[ bool, bytes ]
# float_fn = Callable[ float, bytes ]
# tmst_fn = Callable[ dt.datetime, bytes ]
#
# KeyValFn = Callable[ KeyValTypes, bytes ]
#
# KeyFuncDispatch: type = type[ str_fn, int_fn, bool_fn, float_fn, tmst_fn ]

#VectorValTypes: type = type[ None, str, int, bool, float, dt.datetime ]

