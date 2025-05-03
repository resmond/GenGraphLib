import sys
from collections.abc import AsyncGenerator
from typing import Self

import os
import pickle as pkl
import pyarrow as par
import polars as pol

from src.gengraphlib.common import (
    KeyValTypes,
    KeyInfo,
    VectorValTypes,
    KeyType,
)

from src.gengraphlib.columns import (
    Column,
    StrColumn,
    IntColumn,
    BoolColumn,
    FloatColumn,
    TmstColumn
)

from src.gengraphlib.arrow.ParquetFileIo import write_parquet, read_parquet

ValuesDict: type = dict[str, VectorValTypes ]

class GraphTable:

    def __init__(
            self: Self,
            table_name: str,
            data_dir: str | None = None,
            keys: list[KeyInfo] | None = None ,
            active_keys: set[str] | None = None,
            load_columns: bool = False,
            load_table: bool = False
        ) -> None:

        super().__init__()
        self.table_name: str = table_name
        self.columns:    dict[ str, Column ] = dict[ str, Column]()

        self.data_dir:   str             | None = data_dir
        self.keys:       list[ KeyInfo ]  = list[ KeyInfo ]()

        self.datatable: par.Table | None = None

        self.maxrefcnt = 1000

        for keyinfo in keys:
            if keyinfo.key in active_keys:
                self.keys.append(keyinfo)

        if not self.keys and self.data_dir:
            self.load_info()

        if self.keys:
            self.init_columns(load_columns)

            if load_table:
                self.datatable = read_parquet( self.columns, self.get_filepath() )

    def init_columns(self: Self, load_columns: bool) -> None:
        for keyinfo in self.keys:
            match keyinfo.keytype:
                case KeyType.KStr:
                    self.columns[keyinfo.key] = StrColumn(keyinfo, self.data_dir, load_columns )
                case KeyType.KInt:
                    self.columns[keyinfo.key] = IntColumn(keyinfo, self.data_dir, load_columns)
                case KeyType.KBool:
                    self.columns[keyinfo.key] = BoolColumn(keyinfo, self.data_dir, load_columns)
                case KeyType.KFloat:
                    self.columns[keyinfo.key] = FloatColumn(keyinfo, self.data_dir, load_columns)
                case KeyType.KTmst:
                    self.columns[keyinfo.key] = TmstColumn(keyinfo, self.data_dir, load_columns)

    def get_datatable( self: Self ) -> par.Table:
        if self.datatable is None:
            self.datatable = read_parquet( self.columns, self.get_filepath() )
        return self.datatable

    def get_fieldnames( self: Self ) -> list[str]:
        return [ info.key for info in self.keys ]

    def row_todict( self: Self, rowindex: int, nulls: bool ) -> ValuesDict:
        row_dict = ValuesDict()
        for key, key_column in self.columns.items():
            value: VectorValTypes = key_column.keyvalue_from_recno( rowindex )
            if value or nulls:
                row_dict[ key ] = value
        return row_dict

    async def get_rows( self: Self, start: int = 0, end: int = 0 ) -> AsyncGenerator[ ValuesDict, None ]:
        if end == 0:
            end = self.maxrefcnt

        rowindex: int = start
        while rowindex <= end:
            row: ValuesDict = self.row_todict( rowindex, True )
            yield row
            rowindex += 1

    def getrow_byindex( self: Self, rowindex: int, blank_nulls: bool ):
        row_values: list[ VectorValTypes ] = []

        for key, key_column in self.columns.items():
            value: VectorValTypes = key_column.keyvalue_from_recno( rowindex )
            if value or not blank_nulls:
                row_values.append( value )
            else:
                row_values.append("")

    def gettyped_column[ T: KeyValTypes ]( self: Self, keyid: str ) -> Column[T] | None:
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

    def get_infofilepath( self: Self ) -> str:
        return os.path.join( self.data_dir, f"{self.table_name}.table")

    def get_tablefilepath( self: Self ) -> str:
        return os.path.join( self.data_dir, f"{self.table_name}.parquet")

    def get_arrowfields( self: Self ) -> list[ tuple[ str, par.DataType ] ]:
        return [col.get_arrowfield() for key, col in self.columns ]

    def save_table(self: Self) -> bool:

        return write_parquet( self.columns, self.get_tablefilepath() )

    def read_table( self: Self ) -> par.Table:
        table_path: str = self.get_tablefilepath()
        print(f'GraphTable.read_table( {table_path} )')
        self.datatable = read_parquet( self.columns, table_path  )
        return self.datatable

    def load_info( self: Self ) -> bool:
        try:
            filepath = self.get_infofilepath()
            sys.path.append( "/home/richard/proj/GenGraphLib/src" )
            if os.path.exists(filepath):
                with open( file=filepath, mode="rb" ) as file:
                    keys_obj = pkl.load(file)
                    if isinstance(keys_obj, list):
                        self.keys = keys_obj
                return True
            else:
                return False
        except Exception as exc:
            print(f"GraphTable[{self.table_name}].read_file( {self.get_infofilepath()} ) Exception: {exc}" )
            return False

    def save_info( self: Self ) -> bool:
        try:
            if not os.path.exists( self.data_dir ):
                os.mkdir( self.data_dir )

            with open( self.get_infofilepath(), "wb" ) as writer:
                buffer: bytes = pkl.dumps( self.keys )
                writer.write(buffer)
            return True
        except Exception as exc:
            f"GraphTable[{self.table_name}].write_file( {self.get_infofilepath()} ) Exception: {exc}"
            return False


if __name__ == "__main__":
    graph_table = GraphTable("logevents","/home/richard/data/jctl-logs/boots/25-04-27:22-28/" )
    table: par.Table = graph_table.read_table()
    df: pol.DataFrame = pol.DataFrame(data=table)

