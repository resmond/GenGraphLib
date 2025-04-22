from typing import Self

import os.path
import threading as th
import multiprocessing as mp

from ..common import KeyValTypes
from ..proc.TaskLib import TaskBase, IndexTaskInterface

class IndexTaskBase[ T: KeyValTypes ]( TaskBase, IndexTaskInterface ):

    def __init__(self: Self, key: str, alias: str, root_dir: str ) -> None:
        super(IndexTaskBase,self).__init__( f"{key}-index" )
        #self.key_def:   KeyDefBase   = key_def
        #self.keyvalues: KeyValues[T] = keyvalues

        self._type: type = type(T)
        self._key:   str = key
        self._alias: str = alias
        self._queue: mp.Queue = mp.Queue()
        self._root_dir: str = root_dir
        self.thread: th.Thread = th.Thread(target=self.main_loop, name=self._key, args = (self._queue, self._type, ) )

        self._index_dir: str = os.path.join( root_dir, "keys", f"{self._key}" )
        self._index_filepath: str = os.path.join( self._index_dir, f"{self._key}.bin" )

    @property
    def key( self: Self ) -> str:
        return self._key

    @property
    def alias( self: Self ) -> str:
        return self._alias

    @property
    def index_dir( self: Self ) -> str:
        return self._index_dir

    @property
    def index_filepath( self: Self ) -> str:
        return self._index_filepath

    @property
    def queue( self: Self ) -> mp.Queue:
        return self._queue

    def start( self: Self ) -> None:
        super().start()

    def main_loop( self: Self, queue: mp.Queue, val_type: type ) -> None:
        while True:
            rec_num: int
            value: str
            rec_num, value = queue.get()
            self.recv_value( rec_num, value )

    def recv_value( self: Self, rec_num: int, value: str ) -> None:
        pass



