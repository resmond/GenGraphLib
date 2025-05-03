from typing import Self

import multiprocessing as mp

from . import ModelProperty, ModelInfo

class DataTableModel:

    def __init__( self: Self, mod_id: str | None = None ) -> None:
        super().__init__()

        self.mod_id: str = mod_id
        self.model_info: ModelInfo | None = None
        self.properties: dict[ str, ModelProperty ] | None = None
        self.queuemap:   dict[ str, mp.Queue ] = dict[ str, mp.Queue ]()

    def init_import( self: Self, app_msgqueue: mp.Queue) -> dict[str, mp.Queue] | None:
        if "model" in self.__dict__:
            self.model_info: ModelInfo = self.__dict__["model"]
            self.properties = self.model_info.properties
            for name, prop in self.properties:
                self.importers[ name ] = prop.importer
            for name, prop in self.properties:
                self.queuemap[ name ] = prop.start(app_msgqueue)

            return self.queuemap
        else:
            return None

