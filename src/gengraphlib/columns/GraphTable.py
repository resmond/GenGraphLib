from collections import namedtuple
from collections.abc import Iterable
# from dataclasses import dataclass, field
# from enum import IntEnum
from typing import Self, NamedTuple

import pickle as pk

from ..common import KeyValTypes, KeyInfo, VectorValTypes, KeyValSchemaInfo, BootLogInfo

from ..columns import Column, ColumnsFactory

class VectorResult:

    def __init__( self: Self, _iter: Iterable[ tuple[ str, KeyValTypes ] ] ):
        super().__init__()
        self.__dict__ = { key:value for key,value in vec_iter }

class GraphRow(NamedTuple):
    row_number:   int
    field_values: tuple

class GraphTable:

    def __init__( self: Self, table_name: str, schema_info: KeyValSchemaInfo, bootlog_info: BootLogInfo ) -> None:
        super().__init__()
        self.vec_name: str                    = table_name
        self.schema_info:   KeyValSchemaInfo  = schema_info
        self.bootlog_info:  BootLogInfo       = bootlog_info

        self.keys:     list[ KeyInfo ]        = schema_info.keys
        self.key_cnt:  int                    = len(self.schema_info.keys)
        self.columns:  dict[ str, Column]     = dict[str, Column]()
        self.row_vals: list[ VectorValTypes ] = []

    def init_internals( self: Self ) -> None:
        self.row_vals: list[ VectorValTypes ] = [ None ] * self.key_cnt

        ColumnsFactory.inst.init_table( self )

    def get_datadir( self: Self ) -> str:
        return self.bootlog_info.dir_path

    def get_fieldnames( self: Self ) -> list[str]:
        return [ info.key for info in self.keys ]

    def get_namedtuple( self: Self ) -> namedtuple:
        return namedtuple(self.vec_name, self.field_names )

    def get_typed_namedtuple( self: Self ) -> NamedTuple:
        return NamedTuple(self.vec_name, [('name', str), ('id', int)])

    def to_tuples( self: Self ) -> tuple:
        return tuple( self.row_vals )

    def tup_binary( self: Self ) -> bytes:
        buffer: bytes = pk.dumps( tuple( self.row_vals ) )
        return buffer

    def list_binary( self: Self ) -> bytes:
        buffer: bytes = pk.dumps( self.row_vals )
        return buffer

    def to_namedtuple( self: Self ) -> namedtuple:
        new_named_tuple = self.named_tuple( self.vec_values )
        return new_named_tuple

    def get_delimated_header( self: Self ) -> str:
        return ",".join(self.vec_fieldnames)

    def to_delimited( self: Self ) -> str:
        return ",".join( self.row_vals )

    def getrow_byindex( self: Self, index: int, blank_nulls: bool ):
        row_values: list[ VectorValTypes ] = []

        for key, key_column in self.columns.items():
            value: VectorValTypes = key_column.keyvalue_from_recno( index )
            if value or not blank_nulls:
                row_values.append( value )
            else:
                row_values.append("")

    def gettyped_column[ T: KeyValTypes ]( self: Self, keyid: str ) -> Column[T ] | None:
        if keyid in self.column_map:
            column: Column = self.column_map[ keyid ]
            if column.keyinfo.pytype is type(T):
                return column

        return None

    def get_column( self: Self, keyid: str ) -> Column | None:
        if keyid in self.column_map:
            return self.column_map[ keyid ]
        else:
            return None





if __name__ == "__main__":

    vec_vals: dict[ str, KeyValTypes ] = { "x": "foo", "y": "bar", "k": 5 }

    vec_iter: Iterable[ tuple[ str, KeyValTypes ] ] = (
        ( "x", "foo" ),
        ( "y", "bar" ),
        ( "k", 5     )
    )

    vec_dict: dict = { key:value for key,value in vec_iter }

    vec_result: VectorResult = VectorResult( _iter=vec_iter )

    print( vec_result )
