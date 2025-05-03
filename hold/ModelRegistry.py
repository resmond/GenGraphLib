from typing import Self

from .ModelInfo import ModelInfo

class ModelRegistry:
    models: dict[str, ModelInfo] = {}
    model_classes: dict[str, type] = dict[str, type]()

    @classmethod
    def register_model( cls: Self, model_info: ModelInfo ) -> None:
        cls.models[ model_info.mod_id ] = model_info

    @classmethod
    def init_models( cls: Self ) -> None:
        for model_id, module in cls.models.items():
            module.register_properties()

    @classmethod
    def dump_models( cls: Self ) -> None:
        for model_id, module in cls.models.items():
            print(f'{model_id}  {module.mod_id}')
            print()
            module.dump_props()

    @classmethod
    def register_modelclass( cls: Self, modelclass: type ) -> None:
        cls.model_classes[modelclass.__name__] = modelclass

def table_model( cls: type) -> type:
    class new_modelclass(cls):
        def is_graphmodel( self: Self ) -> bool:
            self.__dict__["_table_model"] = True
            return True

    return new_modelclass
