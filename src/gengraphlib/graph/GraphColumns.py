from typing import Self

from ..common import KeyValSchemaInfo, KeyType, KeyValTypes
from ..columns import (
    Column,
    StrColumn,
    IntColumn,
    BoolColumn,
    FloatColumn,
    TmstColumn
)

class GraphColumns:
    inst: Self

    def __init__( self: Self, root_dir: str ) -> None:
        GraphColumns.inst = self

        self.root_dir: str = root_dir
        self.column_map: dict[str, Column] = dict[str, Column]()

    def init_columns( self: Self, schema_info: KeyValSchemaInfo ) -> None:
        for keyinfo in schema_info.keys:

            match keyinfo.keytype:
                case KeyType.KStr:
                    self.column_map[keyinfo.key] = StrColumn( keyinfo, self.root_dir )
                case KeyType.KInt:
                    self.column_map[keyinfo.key] = IntColumn( keyinfo, self.root_dir )
                case KeyType.KBool:
                    self.column_map[keyinfo.key] = BoolColumn( keyinfo, self.root_dir )
                case KeyType.KFloat:
                    self.column_map[keyinfo.key] = FloatColumn( keyinfo, self.root_dir )
                case KeyType.KTmst:
                    self.column_map[keyinfo.key] = TmstColumn( keyinfo, self.root_dir )

    def get_column[T: KeyValTypes]( self: Self, keyid: str ) -> Column[T] | None:
        if keyid in self.column_map:
            column: Column = self.column_map[ keyid ]
            if column.keyinfo.pytype is type(T):
                return column

        return None


