from typing import Self

from enum import IntEnum

from abc import ABC, abstractmethod

import multiprocessing as mp
from threading import Thread

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

class TaskBase( ABC ):
    default_queue_size: int = 1024 * 256

    def __init__(self: Self, thread_id: str, queue_size: int | None = None ) -> None:
        self.task_id: str = thread_id
        self.queue_size: int = queue_size or self.default_queue_size
        self.msg_queue: mp.SimpleQueue = mp.SimpleQueue()
        self.proc_state: TaskState = TaskState.Init
        self.proc_type: TaskType = TaskType.Undefined
        self.thread: Thread | None = None

    @abstractmethod
    def start(self: Self) -> None: ...

    def stop(self: Self) -> None:
        pass

    def main_loop(self: Self) -> None:
        pass
