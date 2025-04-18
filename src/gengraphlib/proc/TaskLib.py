from asyncio import Protocol
from typing import Self

from enum import IntEnum

from abc import ABC, abstractmethod

import multiprocessing as mp
from   threading import Thread

from ..common import KeyValTypes

class TaskType( IntEnum ):
    Undefined = 0
    Main = 1
    StreamSource = 2
    StreamSink = 3
    KeyValProcessor = 4

class TaskState( IntEnum ):
    Init = 1
    Running = 2
    Stopped = 3

class Startable(Protocol):
    @abstractmethod
    def id( self ) -> str: ...
    @abstractmethod
    def is_proc( self ) -> bool: ...
    def start( self: Self ) -> None: ...
    def stop( self: Self ) -> None: ...
    @abstractmethod
    def main_loop( self: Self ) -> None: ...

class IndexTaskInterface(Protocol, Startable):

    @property
    @abstractmethod
    def key( self: Self ) -> str: ...

    @property
    @abstractmethod
    def alias( self: Self ) -> str: ...

    @property
    @abstractmethod
    def index_dir( self: Self ) -> str: ...

    @property
    @abstractmethod
    def index_filepath( self: Self ) -> str: ...

    @property
    @abstractmethod
    def queue( self: Self ) -> mp.Queue: ...

    def get_tqueue[T: KeyValTypes]( self: Self ) -> mp.Queue[T] | None: ...

    #def start( self: Self ) -> None: ...
    #def stop( self: Self ) -> None: ...

class IndexManagerInterface(Protocol):

    @staticmethod
    def start_indexes() -> None: ...

    @staticmethod
    def stop_indexes() -> None: ...

    @staticmethod
    def register_index( index: IndexTaskInterface ) -> None: ...


class TaskBase( ABC, Startable ):
    default_queue_size: int = 1024 * 256

    def __init__( self: Self, task_id: str, queue_size: int | None = None ) -> None:
        self.queue_size: int = queue_size or self.default_queue_size
        self.task_state: TaskState = TaskState.Init
        self.task_type:  TaskType = TaskType.Undefined
        self.msg_queue:  mp.Queue | None = None
        self.thread:     Thread | None = None
        self.task_id:    str = task_id
        #AppProcessBase.instance.register_proc(self)

    def id( self: Self ) -> str:
        return self.task_id

    def is_proc( self: Self ) -> bool:
        return False

    def start(self: Self) -> None:
        if self.thread is not None:
            self.thread.start()

    def stop(self: Self) -> None:
        if self.thread is not None:
            self.thread.join(timeout=1)

    @abstractmethod
    def main_loop(self: Self) -> None:
        pass
