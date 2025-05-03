from typing import Self
import multiprocessing as mp

from src.gengraphlib.common import TaskType, TaskState

class TaskBase:
    default_queue_size: int = 1024 * 256

    def __init__( self: Self, task_id: str, queue_size: int | None = None ) -> None:
        self.task_id:    str = task_id
        self.queue_size: int = queue_size or self.default_queue_size
        self.task_state: TaskState = TaskState.Init
        self.task_type:  TaskType = TaskType.Undefined
        self.msg_queue:  mp.Queue | None = None
        #AppProcessBase.instance.register_proc(self)

    def id( self: Self ) -> str:
        return self.task_id

    # noinspection PyMethodMayBeStatic
    def is_proc( self: Self ) -> bool:
        return False

