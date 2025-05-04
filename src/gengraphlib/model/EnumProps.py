from typing import Self

from enum import StrEnum, IntEnum

from pyarrow import DataType, utf8, uint8

from .ModelProperty import ModelProperty

class IntEnumModProp[T: IntEnum]( ModelProperty[T] ):
    def __init__(self: Self, name: str|None=None, alias: str|None = None, store_type: DataType = uint8(), **kwargs ) -> None:
        super().__init__( name=name, alias=alias, store_type=store_type, *kwargs )

class StrEnumModProp[T: StrEnum]( ModelProperty[T ] ):
    def __init__(self: Self, name: str|None=None, alias: str|None = None, store_type: DataType = utf8(), **kwargs ) -> None:
        super().__init__( name=name, alias=alias, store_type=store_type, *kwargs )

