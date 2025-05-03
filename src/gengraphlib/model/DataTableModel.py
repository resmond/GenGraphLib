from typing import Self

from . import (
    ModelRegistry,
    ModelProperty,
    ModelImportFilter,
    ModelInfo
)


class DataTableModel:

    def __init__( self: Self, mod_id: str | None = None ) -> None:
        super().__init__()

        self.mod_id: str = mod_id
        self.mod_cls: object = self.__class__
        self.properties: dict[ str, ModelProperty ] | None = None
        self.importers:  dict[ str, ModelImportFilter ] = dict[ str, ModelImportFilter ]()
        ModelRegistry.register_modelclass(self)

    def init_importers( self: Self ) -> bool:
        if hasattr( DataTableModel, "model_info" ):
            self.properties = DataTableModel.model_info.properties

            for key, prop in self.properties.items():

            return True
        else:
            return False

