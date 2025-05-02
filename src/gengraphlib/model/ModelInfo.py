from typing import Self

from .ModelPropertyBase import ModelPropertyBase
from .ModelRegistry import ModelRegistry


class ModelInfo:

    def __init__( self: Self, mod_id: str ) -> None:
        super().__init__()

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
