from typing import Self

from ..common import ModelDictData
from .ModelProperty import ModelProperty

from loguru import logger

class ModelInfo:

    def __init__( self: Self, model_id: str, **kwargs ) -> None:
        super().__init__()
        self.model_id: str = model_id
        self.data: ModelDictData = kwargs if kwargs else ModelDictData()
        
        # if data:
        #     self.data: ModelDictData = data
        # else:
        #     self.data: ModelDictData = {}

        self.properties: dict[ str, ModelProperty ] = dict[str, ModelProperty ]()

    def __set_name__( self: Self, owner: object, name: str ) -> None:
        self.name  = name
        self.mod_cls = owner
        owner.model = self
        owner.cfg = self.data

    def __get__( self: Self, instance: object, owner: object ) -> dict[str, ModelProperty ]:
        return self.properties

    def dump_props( self: Self ) -> None:
        for name, prop in self.properties.items():
            logger.info(f'{self.model_id}[{name}] proptype: {prop.__class__.__name__}  generictype: {prop.ttype} store: {prop.store_type}')
