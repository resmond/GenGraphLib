from __future__ import annotations

from typing import Self, Protocol

from enum import IntEnum

from abc import ABC, abstractmethod

import multiprocessing as mp
from threading import Thread
from ..tasks import TaskBase

class ProcType(IntEnum):
    Undefined = 0
    Main = 1
    StreamSource = 2
    StreamSink = 3
    KeyValProcessor = 4

class ProcState(IntEnum):
    Init = 1
    Running = 2
    Stopped = 3

class ProcRegistry(Protocol):
    instance: Self

    def register_proc( self, proc: ProcBase ) -> None: ...

class ProcBase(ABC):
    default_queue_size: int = 1024 * 256

    def __init__(self: Self, proc_id: str, queue_size: int | None = None ) -> None:
        self.proc_id: str = proc_id
        self.queue_size: int = queue_size or self.default_queue_size
        self.msg_queue: mp.SimpleQueue = mp.SimpleQueue()
        self.proc_state: ProcState = ProcState.Init
        self.proc_type: ProcType = ProcType.Undefined
        self.proc: mp.Process | None = None
        self.main_thread: Thread | None = None
        self.tasks: dict[str, TaskBase ] = {}
        ProcRegistry.instance.register_proc(self)

    @abstractmethod
    def start(self: Self) -> None: ...

    def main_loop(self: Self) -> None:
        pass

    def stop(self: Self) -> None:
        pass

    def register_task( self, task: TaskBase ) -> None:
        self.tasks[ task.task_id ] = task

    def start_task( self, task_id: str ) -> None:
        if task_id in self.tasks:
            task_thread = self.tasks[task_id ]
            task_thread.start()
        else:
            #throw_error(f"[ProcBase.start_task] Unknown Task ID: {task_id}")
            print(f"[ProcBase.start_task] Unknown Task ID: {task_id}")







