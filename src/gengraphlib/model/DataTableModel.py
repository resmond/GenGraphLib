from typing import Self

import multiprocessing as mp

from . import (
    ModelRegistry,
    ModelProperty,
    ModelImportFilter
)


class DataTableModel:

    def __init__( self: Self, mod_id: str | None = None ) -> None:
        super().__init__()

        self.mod_id: str = mod_id
        self.mod_cls: object = self.__class__
        self.properties: dict[ str, ModelProperty ] | None = None
        self.importers:  dict[ str, ModelImportFilter ] = dict[ str, ModelImportFilter ]()

        ModelRegistry.register_modelclass(self)

    def init_import( self: Self, app_msgqueue: mp.Queue) -> dict[str, mp.Queue] | None:
        import_queues: dict[str, mp.Queue] = {}
        if hasattr( DataTableModel, "model_info" ):
            self.properties = DataTableModel.model_info.properties
            for key, prop in self.properties.items():
                import_queue = prop.init_import( app_msgqueue )
                if import_queue:
                    import_queues[key] = import_queue
                else:
                    return None
            return import_queues
        else:
            return None



