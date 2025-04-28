from collections.abc import AsyncGenerator
from typing import Self

import os
import pickle as pkl

from ..common import (
    KeyValTypes,
    KeyInfo,
    VectorValTypes,
    KeyType,
)

from ..columns import (
    Column,
    StrColumn,
    IntColumn,
    BoolColumn,
    FloatColumn,
    TmstColumn
)

GraphRow: type = dict[str, VectorValTypes]

class GraphTable:

    def __init__( self: Self, table_name: str, data_dir: str | None = None, keys: list[KeyInfo] | None = None ) -> None:
        super().__init__()
        self.table_name: str = table_name
        self.columns:    dict[ str, Column ] = dict[ str, Column ]()

        self.data_dir:   str             | None = data_dir
        self.keys:       list[ KeyInfo ] | None = keys

        match self:
            case self.keys:
                self.init_columns()
            case data_dir:
                self.read_file()
                self.init_columns()

    def init_columns(self: Self) -> None:
        for keyinfo in self.keys:
            match keyinfo.keytype:
                case KeyType.KStr:
                    self.columns[keyinfo.key] = StrColumn(keyinfo, self.data_dir )
                case KeyType.KInt:
                    self.columns[keyinfo.key] = IntColumn(keyinfo, self.data_dir)
                case KeyType.KBool:
                    self.columns[keyinfo.key] = BoolColumn(keyinfo, self.data_dir)
                case KeyType.KFloat:
                    self.columns[keyinfo.key] = FloatColumn(keyinfo, self.data_dir)
                case KeyType.KTmst:
                    self.columns[keyinfo.key] = TmstColumn(keyinfo, self.data_dir)

    def get_filepath( self: Self ) -> str:
        return os.path.join( self.data_dir, f"{self.table_name}-info.obj")

    def get_fieldnames( self: Self ) -> list[str]:
        return [ info.key for info in self.keys ]

    def get_delimated_header( self: Self ) -> str:
        return ",".join(self.vec_fieldnames)

    def to_delimited( self: Self ) -> str:
        return ",".join( self.row_vals )

    def row_todict( self: Self, rowindex: int, nulls: bool ) -> GraphRow:
        row_dict = GraphRow()
        for key, key_column in self.columns.items():
            value: VectorValTypes = key_column.keyvalue_from_recno( rowindex )
            if value or nulls:
                row_dict[ key ] = value
        return row_dict

    async def get_rows( self: Self, start: int = 0, end: int = 0 ) -> AsyncGenerator[ GraphRow, None ]:
        if end == 0:
            end = self.maxrefcnt

        for rowindex in range( start, end ):
            row: GraphRow = self.row_todict(rowindex, True)
            yield row

    def getrow_byindex( self: Self, rowindex: int, blank_nulls: bool ):
        row_values: list[ VectorValTypes ] = []

        for key, key_column in self.columns.items():
            value: VectorValTypes = key_column.keyvalue_from_recno( rowindex )
            if value or not blank_nulls:
                row_values.append( value )
            else:
                row_values.append("")

    def gettyped_column[ T: KeyValTypes ]( self: Self, keyid: str ) -> Column[T ] | None:
        if keyid in self.columns:
            column: Column = self.columns[ keyid ]
            if column.keyinfo.pytype is type(T):
                return column

        return None

    def get_column( self: Self, keyid: str ) -> Column | None:
        if keyid in self.columns:
            return self.columns[ keyid ]
        else:
            return None

    def read_file( self: Self ) -> bool:
        try:
            with open( self.get_filepath(), "b" ) as reader:
                keys_obj: list[KeyInfo] = pkl.load(reader)
                self.keys = keys_obj
            return True
        except Exception as exc:
            print(f"GraphTable[{self.table_name}].read_file( {self.get_filepath()} ) Exception: {exc}")
            return False

    def write_file( self: Self ) -> bool:
        try:
            if not os.path.exists( self.data_dir ):
                os.mkdir( self.data_dir )

            with open( self.get_filepath(), "wb" ) as writer:
                buffer: bytes = pkl.dumps( self.keys )
                writer.write(buffer)
            return True
        except Exception as exc:
            f"GraphTable[{self.table_name}].write_file( {self.get_filepath()} ) Exception: {exc}"
            return False



