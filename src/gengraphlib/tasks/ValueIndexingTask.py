from typing import Self

from ..proc.TaskLib import TaskBase

class ValueIndexingTask( TaskBase ):

    def __init__(self: Self, proc_id: str, queue_size: int | None = None ) -> None:
        super( ValueIndexingTask, self ).__init__( proc_id, queue_size )

    def start( self: Self ) -> None:
        pass

    def main_loop(self: Self) -> None:
        pass
