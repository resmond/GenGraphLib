from __future__ import annotations
from typing import Self, Protocol

from enum import StrEnum, IntEnum

import datetime as dt

from pyarrow import utf8, int64, date32, DataType, uint8, bool_

ModelPropTypes: type = type[ str, int, float, dt.datetime, StrEnum, IntEnum, bool]

class ModelRegistry:
    models: dict[str, ModelInfo] = {}

    @classmethod
    def register_model( cls, model_info: ModelInfo ) -> None:
        cls.models[ model_info.mod_id ] = model_info

    @classmethod
    def init_models( cls ) -> None:
        for model_id, module in cls.models.items():
            module.register_properties()

    @classmethod
    def dump_models( cls ) -> None:
        for model_id, module in cls.models.items():
            print(f'{model_id}  {module.mod_id}')
            print()
            module.dump_props()



class ModelInfo:

    def __init__( self: Self, mod_id: str ) -> None:
        self.properties: dict[ str, ModelPropertyBase ] = dict[str, ModelPropertyBase]()
        self.mod_id: str = mod_id
        self.mod_cls: object = self.__class__
        ModelRegistry.register_model(self)

    def __set_name__( self: Self, owner: object, name: str ) -> None:
        self.name  = name
        self.mod_cls = owner

    def __get__( self: Self, instance: object, owner: object ) -> dict[str, ModelPropertyBase]:
        return self.properties

    def __set__( self: Self, instance: object, value: dict[str, ModelPropertyBase] ) -> None:
        pass

    def register_properties( self: Self ) -> None:
        for name, prop in self.mod_cls.__dict__.items():
            match prop:
                case ModelPropertyBase():
                    self.properties[prop.name] = prop
                    #print(f'{name}({prop.name})  mod_id: {prop.mod_id}  ttype: {prop.ttype}  import: {prop.import_type}  store: {prop.store_type}  dict: {prop.use_dict}')
                case _:
                    pass

    def dump_props( self: Self ) -> None:
        for name, prop in self.properties.items():
            print(f'{name}({prop.name})  mod_id: {prop.mod_id}  ttype: {prop.ttype}  import: {prop.import_type}  store: {prop.store_type}  dict: {prop.use_dict}')





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
                self.model.register_property(self)

    def __get__( self: Self, instance: object, owner: object ) -> T:
        return instance.__dict__[self.name]

    def __set__( self: Self, instance: object, value: T ) -> None:
        instance.__dict__[self.name] = value

class StrModProp( ModelPropertyBase[str] ):
    def __init__(
        self: Self,
        mod_id: str | None = None,
        *,
        import_type: DataType = utf8(),
        store_type: DataType = uint8(),
        alias: str | None = None,
        use_dict: bool = False
    ) -> None:

        super().__init__( mod_id=mod_id, import_type=import_type, store_type=store_type, alias=alias, use_dict=use_dict )

class BranchModProp( ModelPropertyBase[str] ):
    def __init__(
        self: Self,
        mod_id: str | None = None,
        *,
        import_type: DataType = utf8(),
        store_type: DataType = uint8(),
        alias: str | None = None
    ) -> None:

        super().__init__( mod_id=mod_id, import_type=import_type, store_type=store_type, alias=alias, use_dict=True )

class IntModProp( ModelPropertyBase[int]):
    def __init__(
        self: Self,
        mod_id: str | None = None,
        *,
        import_type: DataType = int64(),
        store_type: DataType = uint8(),
        alias: str | None = None,
        use_dict: bool = False
    ) -> None:

        super().__init__( mod_id=mod_id, import_type=import_type, store_type=store_type, alias=alias, use_dict=use_dict )


class TmstModProp(ModelPropertyBase[dt.datetime]):
    def __init__( self: Self,
                  mod_id: str | None = None,
                  *,
                  alias: str | None = None,
                  import_type: DataType = int64(),
                  store_type:  DataType = date32(),
                  use_dict: bool = False
                  ) -> None:

        super().__init__( mod_id=mod_id, import_type=import_type, store_type=store_type, alias=alias, use_dict=use_dict )

class StrEnumModProp[T: StrEnum]( ModelPropertyBase[T] ):
    def __init__(
            self: Self,
            mod_id: str | None = None,
            *,
            alias: str | None = None,
            store_type:  DataType = uint8(),
        ) -> None:

        super().__init__( mod_id=mod_id, import_type=utf8(), store_type=store_type, alias=alias, use_dict=True )

class IntEnumModProp[T: IntEnum]( ModelPropertyBase[T] ):
    def __init__(
            self: Self,
            mod_id: str | None = None,
            *,
            store_type:  DataType = uint8(),
            alias: str | None = None,
        ) -> None:

        super().__init__( mod_id=mod_id, import_type=int64(), store_type=store_type, alias=alias, use_dict=True )

class BoolModProp( ModelPropertyBase[bool] ):
    def __init__(
            self: Self,
            mod_id: str | None = None,
            *,
            alias: str | None = None,
        ) -> None:

        super().__init__( mod_id =mod_id, import_type=int64(), store_type=bool_(), alias=alias )


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
