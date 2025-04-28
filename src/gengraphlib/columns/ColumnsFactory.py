from ..common import  KeyType, KeyInfo
from ..columns import (
    Column,
    StrColumn,
    IntColumn,
    BoolColumn,
    FloatColumn,
    TmstColumn
)

class ColumnsFactory:

    @staticmethod
    def column_from_keyinfo( keyinfo: KeyInfo, datadir: str ) -> Column | None:
        match keyinfo.keytype:
            case KeyType.KStr:
                return StrColumn( keyinfo, datadir )
            case KeyType.KInt:
                return IntColumn( keyinfo, datadir )
            case KeyType.KBool:
                return BoolColumn( keyinfo, datadir )
            case KeyType.KFloat:
                return FloatColumn( keyinfo, datadir )
            case KeyType.KTmst:
                return TmstColumn( keyinfo, datadir )

        return None

    @staticmethod
    def init_columns( keyinfo_list: list[KeyInfo], datadir: str ) -> dict[str, Column]:
        columns = dict[str,Column]()
        for keyinfo in keyinfo_list:
            columns[keyinfo.key] = ColumnsFactory.column_from_keyinfo( keyinfo, datadir )
        return columns

