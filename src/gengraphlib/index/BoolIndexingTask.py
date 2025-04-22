from typing import Self
import threading as th
import multiprocessing as mp

from sortedcontainers import SortedSet

from .IndexTaskBase import IndexTaskBase

class BoolIndexingTask( IndexTaskBase[bool] ):
    def __init__( self: Self, key: str, alias: str, root_dir: str  ) -> None:
        super( BoolIndexingTask, self ).__init__(key, alias, root_dir)
        self.positive_intersection: SortedSet[int] = SortedSet[int]()
        self.negative_intersection: SortedSet[int] = SortedSet[int]()
        self.thread: th.Thread = th.Thread(target=self.main_loop, name=self._key, args = (self._queue, self._type, ) )

    def start( self: Self ) -> None:
        self.thread.start()

    def main_loop( self: Self, queue: mp.Queue, val_type: type ) -> None:
        while True:
            rec_num: int
            value: str
            rec_num, value = queue.get()
            self.recv_value( rec_num, value )

    def recv_value( self: Self, rec_num: int, value: str ) -> None:
        try:
            bool_value: bool = bool( value )

            if bool_value:
                self.positive_intersection.add( rec_num )
            else:
                self.negative_intersection.add( rec_num )

        except ValueError:
            print(f"BoolIndexingTask.recv_value - rec_num: {rec_num}  value: {value}")


