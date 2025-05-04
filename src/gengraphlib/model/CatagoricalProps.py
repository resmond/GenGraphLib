from typing import Self

from pyarrow import DataType, utf8

from .ModelProperty import ModelProperty

class ParentModProp( ModelProperty[str ] ):
    def __init__(self: Self, name: str|None=None, alias: str|None = None, store_type: DataType = utf8(), **kwargs ) -> None:
        super().__init__( name=name, alias=alias, store_type=store_type, *kwargs  )

