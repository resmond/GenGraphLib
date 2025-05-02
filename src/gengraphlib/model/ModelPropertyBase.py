from __future__ import annotations
from typing import Self

from pyarrow import DataType

from ..common import ModelPropTypes
from .ModelInfo import ModelInfo


class ModelPropertyBase[T: ModelPropTypes ]:

    def __init__( self: Self, mod_id: str | None, import_type: DataType, store_type: DataType, alias: str | None, use_dict: bool = False ) -> None:
        super().__init__()
        self.model:     ModelInfo | None = None
        self.ttype:     type = type(T)
        self.mod_id:    str    | None = mod_id
        self.name:      str    | None = mod_id
        self.alias:     str    | None = alias
        self.owner:     object | None = None
        self.import_type: DataType = import_type
        self.store_type:  DataType = store_type
        self.use_dict: bool = use_dict

    def __set_name__( self: Self, owner: object, name: str ) -> None:
        self.name  = name
        self.owner = owner

        if hasattr( self.owner, "model_info" ):
            self.model = self.owner.model_info
            if isinstance( self.model, ModelInfo ):
                self.model.register_properties()

    def __get__( self: Self, instance: object, owner: object ) -> T:
        return instance.__dict__[self.name]

    def __set__( self: Self, instance: object, value: T ) -> None:
        instance.__dict__[self.name] = value



# class ModelPropertyInterface(Protocol):
#
#     def __init__( self: Self ) -> None:
#
#         #super().__init__()
#         self.model:     ModelInfo | None = None
#         self.ttype:     type   | None = None
#         self.mod_id:    str    | None = None
#         self.name:      str    | None = None
#         self.alias:     str    | None = None
#         self.owner:     object | None = None
#         self.import_type: DataType
#         self.store_type:  DataType
#         self.use_dict: bool
