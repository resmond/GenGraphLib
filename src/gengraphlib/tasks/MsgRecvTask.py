from typing import Self

from ..proc import TaskBase
from ..proc.MsgQueueBase import MsgQueueBase, StatusMsg, InfoMsg, DataMsg, ErrorMsg

class MsgRecvTask( TaskBase, MsgQueueBase ):
    def __init__(self: Self, proc_id: str, queue_size: int | None = None) -> None:
        super( MsgRecvTask, self ).__init__( proc_id, queue_size )

    def start(self: Self) -> None:
        pass

    def main_loop(self: Self) -> None:
        pass

    def recv_status( self: Self, msg: StatusMsg ) -> None:
        pass

    def recv_info( self: Self, msg: InfoMsg ) -> None:
        pass

    def recv_error( self: Self, msg: ErrorMsg ) -> None:
        pass

    def recv_data( self: Self, msg: DataMsg ) -> None:
        pass


