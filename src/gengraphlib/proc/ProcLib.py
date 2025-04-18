from __future__ import annotations

from typing import Self, Protocol

from enum import IntEnum

from abc import ABC, abstractmethod

import multiprocessing as mp
from   threading import Thread

from .TaskLib import TaskBase
from .AppProcessBase import Startable
from .. import AppProcessBase


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
    def register_proc( self, proc: ProcBase ) -> None: ...

class ProcBase(ABC, Startable):
    default_queue_size: int = 1024 * 256

    def __init__(self: Self, proc_id: str, queue_size: int | None = None ) -> None:
        self.proc_id: str = proc_id
        self.queue_size: int = queue_size or self.default_queue_size
        self.msg_queue: mp.SimpleQueue = mp.SimpleQueue()
        self.proc_state: ProcState = ProcState.Init
        self.proc_type: ProcType = ProcType.Undefined
        self.process: mp.Process = mp.Process( target = self.main_loop, args=() )
        self.main_thread: Thread | None = None
        self.tasks: dict[str, TaskBase ] = {}
        AppProcessBase.instance.register_startable(self)

    def id( self ) -> str:
        return self.proc_id

    def is_proc( self ) -> bool:
        return True

    def start(self: Self) -> None:
        self.process.start()

    @abstractmethod
    def main_loop(self: Self) -> None:
        pass

    def stop(self: Self) -> None:
        self.process.terminate()
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







