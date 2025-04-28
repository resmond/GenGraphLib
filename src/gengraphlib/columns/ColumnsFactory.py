from typing import Self

from ..common import  KeyType
from ..columns import (
    StrColumn,
    IntColumn,
    BoolColumn,
    FloatColumn,
    TmstColumn,
    GraphTable
)


class ColumnsFactory:
    inst: Self

    def __init__( self: Self, root_dir: str ) -> None:
        ColumnsFactory.inst = self

        self.root_dir: str = root_dir

    def init_table( self: Self, graph_table: GraphTable ) -> None:
        for keyinfo in graph_table.keys:

            match keyinfo.keytype:
                case KeyType.KStr:
                    self.column_map[keyinfo.key] = StrColumn( keyinfo, graph_table )
                case KeyType.KInt:
                    self.column_map[keyinfo.key] = IntColumn( keyinfo, graph_table )
                case KeyType.KBool:
                    self.column_map[keyinfo.key] = BoolColumn( keyinfo, graph_table )
                case KeyType.KFloat:
                    self.column_map[keyinfo.key] = FloatColumn( keyinfo, graph_table )
                case KeyType.KTmst:
                    self.column_map[keyinfo.key] = TmstColumn( keyinfo, graph_table )

    # def gettyped_column[ T: KeyValTypes ]( self: Self, keyid: str ) -> Column[T ] | None:
    #     if keyid in self.column_map:
    #         column: Column = self.column_map[ keyid ]
    #         if column.keyinfo.pytype is type(T):
    #             return column
    #
    #     return None
    #
    # def get_column( self: Self, keyid: str ) -> Column | None:
    #     if keyid in self.column_map:
    #         return self.column_map[ keyid ]
    #     else:
    #         return None


