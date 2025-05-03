from typing import Self

import threading as th
import multiprocessing as mp
from ..common import ModelPropTypes

from . import ModelProperty

class ModelImportFilter[ T: ModelPropTypes ]:

    def __init__( self: Self, prop: ModelProperty ) -> None:

        super().__init__()

        self.prop:  ModelProperty = prop

        self._queue: mp.Queue = mp.Queue()

        self.app_msgqueue: mp.Queue | None = None
        self.thread:      th.Thread | None = None

        self.status_triggercnt: int     = 5000

    @property
    def queue( self: Self ) -> mp.Queue:
        return self._queue

    def start(self: Self, app_msgqueue: mp.Queue ) -> mp.Queue:
        self.app_msgqueue = app_msgqueue
        self.thread = th.Thread(
            target=self.main_loop,
            name=f"{self.prop.name}-index",
            args = (self._queue,)
        )
        self.thread.start()

        return self._queue

    def main_loop( self: Self, queue: mp.Queue ) -> None:
        #keyindex_info: keyIndexInfo = self.get_index_info()
        #self.app_msgqueue.put( keyindex_info )
        print(f'[{self.prop.name}-index]: Started' )
        try:
            while True:   #not end_event:
                rownum, value = queue.get()

                if rownum == -1:
                    self.prop.finalize(int(value))
                    break

                self.prop.recv_value( rownum, value )

                if rownum % self.status_triggercnt == 0:
                    #keyindex_info: keyIndexInfo = self.get_index_info()
                    #self.app_msgqueue.put( keyindex_info )
                    print(f'ModelImport({self.prop.name}:{self.prop.alias}) refs: {rownum}' )

        except ValueError as valexc:
            print(f'ModelImport({self.prop.name}:{self.prop.alias}) ValueError: {valexc}' )

        except Exception as exc:
            print(f'ModelImport({self.prop.name}:{self.prop.alias}) Exception: {exc}' )

        print(f'ModelImport({self.prop.name}:{self.prop.alias}) Done' )





