from typing import Self

import multiprocessing as mp

from . import ModelProperty, ModelInfo
from .. import ModelDictData
from ..arrow import ArrowResults

class DataTableModel:

    def __init__( self: Self, model_id: str | None = None, **kwargs ) -> None:
        super().__init__()

        self.model_id: str = model_id
        self.model_info: ModelInfo | None = None
        self.queuemap:   dict[ str, mp.Queue ] = dict[ str, mp.Queue ]()
        self.data: ModelDictData = kwargs if kwargs else ModelDictData()

        self.properties: dict[ str, ModelProperty ] | None = self.model
        
        classdict = self.__class__.__dict__
        self.model_info = classdict["model"] if "model" in classdict else None
        self.model_id = self.model_info.model_id
        
        self.data.update(self.cfg)

    def init_import( self: Self, app_msgqueue: mp.Queue) -> dict[str, mp.Queue] | None:

        for name, prop in self.properties.items():
            self.queuemap[ prop.alias ] = prop.start_import( app_msgqueue )

        return self.queuemap

    def wait_tocomplete( self: Self ) -> None:
        for name, prop in self.properties.items():
            thr = prop.get_thread()
            thr.join()

    def save_table( self: Self, filepath: str | None = None ):
        ArrowResults.write_arrowtable( self.model_id, filepath )



