from typing import Self, Protocol

from .ModelProperty import ModelProperty
#from .. import DataTableModel


#from .ModelRegistry import ModelRegistry

class ModelRegistryInterface(Protocol):

    @classmethod
    def register_model( cls, name:str, model_info: object ) -> None: ...

class ModelInfo:
    models:          dict[str, Self]           = {}
#    model_classes:   dict[str, type]           = {}
#    model_instances: dict[str, DataTableModel] = {}

    def __init__( self: Self, mod_id: str ) -> None:
        super().__init__()

        self.properties: dict[ str, ModelProperty ] = dict[str, ModelProperty ]()
        self.mod_id: str = mod_id
        ModelInfo.models[ self.mod_id ] = self

    def __set_name__( self: Self, owner: object, name: str ) -> None:
        self.name  = name
        self.mod_cls = owner

    def __get__( self: Self, instance: object, owner: object ) -> dict[str, ModelProperty ]:
        return self.properties

    def __set__( self: Self, instance: object, value: dict[str, ModelProperty ] ) -> None:
        pass

    def register_properties( self: Self ) -> None:
        for name, prop in self.mod_cls.__dict__.items():
            match prop:
                case ModelProperty():
                    self.properties[prop.name] = prop
                    #print(f'{name}({prop.name})  mod_id: {prop.mod_id}  ttype: {prop.ttype}  import: {prop.import_type}  store: {prop.store_type}  dict: {prop.use_dict}')
                case _:
                    pass

    def dump_props( self: Self ) -> None:
        for name, prop in self.properties.items():
            print(f'{name}({prop.name})  mod_id: {prop.mod_id}  ttype: {prop.ttype}  import: {prop.import_type}  store: {prop.store_type}  dict: {prop.use_dict}')
