from typing import Self

from enum import StrEnum, IntEnum

from pyarrow import DataType, utf8, uint8

from .ModelProperty import ModelProperty

class IntEnumModProp[T: IntEnum]( ModelProperty[int] ):
    def __init__(self: Self, name: str|None=None, alias: str|None = None, store_type: DataType = uint8(), **kwargs ) -> None:
        super().__init__( name=name, alias=alias, store_type=store_type, *kwargs )

    def recv_value( self: Self, row_num: int, import_value: str ) -> None:

        if len(import_value) > 0:
            int_value = int(import_value)
        else:
            int_value = 0

        super().recv_value( row_num, int_value )

    def finalize( self: Self, maxrownum: int ) -> None:
        super().finalize( maxrownum )


class StrEnumModProp[T: StrEnum]( ModelProperty[T ] ):
    def __init__(self: Self, name: str|None=None, alias: str|None = None, store_type: DataType = utf8(), **kwargs ) -> None:
        super().__init__( name=name, alias=alias, store_type=store_type, *kwargs )

    def recv_value( self: Self, row_num: int, import_value: str ) -> None:
        super().recv_value( row_num, import_value )

    def finalize( self: Self, maxrownum: int ) -> None:
        super().finalize( maxrownum )
