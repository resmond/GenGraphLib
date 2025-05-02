from typing import Self

import threading as th
import multiprocessing as mp
from ..common import (
    KeyType,
    KeyInfo,
    keyIndexInfo,
    BootLogInfo
)

from ..graphs import GraphTable

class ModelImporter:

    def __init__(
            self: Self,
            key_info:     KeyInfo,
            bootlog_info: BootLogInfo,
            graph_table:  GraphTable,
            app_msgqueue: mp.Queue,
            end_event:    mp.Event
    ) -> None:

        super().__init__()

        self.status_cnt: int     = 100

        self.key_info:     KeyInfo      = key_info
        self.bootlog_info: BootLogInfo  = bootlog_info
        self.graph_table:  GraphTable   = graph_table
        self.app_msgqueue: mp.Queue     = app_msgqueue
        self.end_event:    mp.Event     = end_event

        self.boot_id:    str = self.bootlog_info.boot_id
        self.keyinfo_id: str = f"{self.boot_id}@{key_info.key}"

        self.key:        str     = key_info.key
        self.alias:      str     = key_info.alias
        self.keytype :   KeyType = key_info.keytype

        self._queue: mp.Queue = mp.Queue()

        self.thread: th.Thread = th.Thread(
            target=self.main_loop,
            name=f"{self.key}-Str-index",
            args = (self.queue, self.end_event,)
        )

    @property
    def queue( self: Self ) -> mp.Queue:
        return self._queue

    def start(self: Self) -> None:
        self.thread.start()

    def main_loop( self: Self, queue: mp.Queue, end_event: mp.Event ) -> None:
        keyindex_info: keyIndexInfo = self.get_index_info()
        self.app_msgqueue.put( keyindex_info )
        print(f'[{self.key}-index]: Started')
        try:
            while True:   #not end_event:
                rec_num, value = queue.get()

                if rec_num == -1:
                    self.apply_tocolumn(int(value))
                    break


                if rec_num % self.status_cnt == 0:
                    keyindex_info: keyIndexInfo = self.get_index_info()
                    self.app_msgqueue.put( keyindex_info )
                    #print(f'StrIndexing: {keyindex_info}')

        except ValueError as valexc:
            print(f'ModelImport({self.key}:{self.alias}) ValueError: {valexc}' )

        except Exception as exc:
            print(f'ModelImport({self.key}:{self.alias}) Exception: {exc}')

        print(f'ModelImport({self.key}:{self.alias}) Done')





