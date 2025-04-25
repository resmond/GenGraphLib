from typing import Self
from abc import ABC, abstractmethod

import multiprocessing as mp

from   threading import Thread

from ..common import Startable, ProcType, ProcState

from .TaskLib import TaskBase


class ProcBase(ABC, Startable):
    default_queue_size: int = 1024 * 256

    def __init__(self: Self, proc_id: str ) -> None:
        self.proc_id: str = proc_id
        self.queue_size: int = self.default_queue_size
        self.msg_queue: mp.SimpleQueue = mp.SimpleQueue()
        self.proc_state: ProcState = ProcState.Init
        self.proc_type: ProcType = ProcType.Undefined
        self.process: mp.Process = mp.Process( name=proc_id, target = self.main_loop, args=() )
        self.main_thread: Thread | None = None
        self.tasks: dict[str, TaskBase ] = {}
        #AppProcessBase.instance.register_startable(self)

    def id( self: Self ) -> str:
        return self.proc_id

    # noinspection PyMethodMayBeStatic
    def is_proc( self: Self ) -> bool:
        return True

    def start(self: Self) -> None:
        self.process.start()

    @abstractmethod
    def main_loop(self: Self, *args, **kargs) -> None:
        pass

    def stop(self: Self) -> None:
        self.process.terminate()
        pass

    def register_task( self: Self, task: TaskBase ) -> None:
        self.tasks[ task.task_id ] = task

    def start_task( self, task_id: str ) -> None:
        if task_id in self.tasks:
            pass
            # task_thread = self.tasks[task_id ]
            # task_thread.start()
        else:
            #throw_error(f"[ProcBase.start_task] Unknown Task ID: {task_id}")
            print(f"[ProcBase.start_task] Unknown Task ID: {task_id}")







