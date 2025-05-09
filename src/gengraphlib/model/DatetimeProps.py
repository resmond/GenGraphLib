from typing import Self

import datetime as dt

from pyarrow import DataType, date64

from .ModelProperty import ModelProperty


class TmstModProp( ModelProperty[dt.datetime] ):
    very_beginning = dt.datetime.fromisoformat("1970-01-01")

    def __init__( self: Self, name: str|None=None, alias: str | None = None, store_type: DataType = date64(), **kwargs ) -> None:
        super().__init__( name=name, alias=alias, store_type=store_type, *kwargs )

    def recv_value( self: Self, row_num: int, import_value: str ) -> None:
        int_value = int(import_value)
        datetime_value: dt.datetime = TmstModProp.very_beginning + dt.timedelta(microseconds=int_value)
        super().recv_value( row_num, datetime_value )

    def finalize( self: Self, maxrownum: int ) -> None:
        super().finalize( maxrownum )
