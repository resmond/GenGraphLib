from typing import Self

from pyarrow import DataType, utf8, int64, bool_, float64

from .ModelProperty import ModelProperty

class StrModProp( ModelProperty[ str] ):
    def __init__(self: Self, name: str|None=None, alias: str|None = None, store_type: DataType = utf8(), **kwargs ) -> None:
        super().__init__( name=name, alias=alias, store_type=store_type, *kwargs )

class IntModProp( ModelProperty[ int ] ):
    def __init__(self: Self, name: str|None=None, alias: str|None = None, store_type: DataType = int64(), **kwargs ) -> None:
        super().__init__( name=name, alias=alias, store_type=store_type, *kwargs )

class BoolModProp( ModelProperty[ bool] ):
    def __init__(self: Self, name: str|None=None, alias: str|None = None, **kwargs ) -> None:
        super().__init__( name=name, alias=alias, store_type=bool_(), *kwargs )

class FloatModProp( ModelProperty[ float ] ):
    def __init__(self: Self, name: str|None=None, alias: str|None = None, store_type: DataType = float64(), **kwargs ) -> None:
        super().__init__( name=name, alias=alias, store_type=store_type, *kwargs )

