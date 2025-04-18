from typing import Self

import os.path
import threading as th
import datetime as dt
import multiprocessing as mp

from ..common import KeyValTypes
from ..proc.TaskLib import TaskBase, IndexTaskInterface
from ..graph.KeyDefs import (
    StrKeyDef,
    IntKeyDef,
    BoolKeyDef,
    FloatKeyDef,
    TmstKeyDef,
)
from ..graph.KeyValues import (
    StrKeyValueSet,
    IntKeyValueSet,
    BoolKeyValueSet,
    FloatKeyValueSet,
    TmstKeyValueSet,
)


class IndexTaskBase[ T: KeyValTypes ]( TaskBase, IndexTaskInterface ):


    def __init__(self: Self, key: str, alias: str, root_dir: str ) -> None:
        super(IndexTaskBase,self).__init__( f"{key}-index" )
        #self.key_def:   KeyDefBase   = key_def
        #self.keyvalues: KeyValues[T] = keyvalues
        self._key:   str = key
        self._alias: str = alias
        self._queue: mp.Queue[T] = mp.Queue[T]()
        self._root_dir: str = root_dir
        self.thread: th.Thread = th.Thread(target=self.main_loop, name=self._key)

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

    def get_tqueue[T]( self: Self ) -> mp.Queue[T]:
        return self._queue

    def start( self: Self ) -> None:
        super().start()

    def main_loop( self: Self, safe_queue: mp.Queue[T] ) -> None:
        while True:
            rec_num, value = safe_queue.get()
            self.recv_value(rec_num, value)

    def recv_value( self: Self, rec_num: int, value: T ) -> None:
        pass

class StrIndexingTask( IndexTaskBase[str] ):
    def __init__( self: Self, key_def: StrKeyDef, keyvalues: StrKeyValueSet ) -> None:
        super( StrIndexingTask, self ).__init__( key_def, keyvalues )

    def recv_value[str]( self: Self, rec_num: int, buffer: bytes, value: str ) -> None:
        pass

class IntIndexingTask( IndexTaskBase[int] ):
    def __init__( self: Self, key_def: IntKeyDef, keyvalues: IntKeyValueSet ) -> None:
        super( IntIndexingTask, self ).__init__( key_def, keyvalues )

    def recv_value( self: Self, rec_num: int, buffer: bytes, value: int ) -> None:
        pass

class BoolIndexingTask( IndexTaskBase[bool] ):
    def __init__( self: Self, key_def: BoolKeyDef, keyvalues: BoolKeyValueSet ) -> None:
        super( BoolIndexingTask, self ).__init__( key_def, keyvalues )

    def recv_value( self: Self, rec_num: int, buffer: bytes, value: bool ) -> None:
        pass

class FloatIndexingTask( IndexTaskBase[float] ):
    def __init__( self: Self, key_def: FloatKeyDef, keyvalues: FloatKeyValueSet ) -> None:
        super( FloatIndexingTask, self ).__init__( key_def, keyvalues )

    def recv_value( self: Self, rec_num: int, buffer: bytes, value: float ) -> None:
        pass

class TmstIndexingTask( IndexTaskBase[dt.datetime] ):
    def __init__( self: Self, key_def: TmstKeyDef, keyvalues: TmstKeyValueSet ) -> None:
        super( TmstIndexingTask, self ).__init__( key_def, keyvalues )

    def recv_value( self: Self, rec_num: int, buffer: bytes, value: dt.datetime ) -> bool:
        pass
