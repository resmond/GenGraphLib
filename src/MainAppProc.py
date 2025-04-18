from typing import Self

from BootLogSchema import BootLogSchema
from src.gengraphlib import (
    StatusMsg,
    InfoMsg,
    ErrorMsg,
    DataMsg,
    KeyValueSchema,
    MsgQueueBase,
)
from src.gengraphlib.proc import AppProcessBase

class MainAppProc( AppProcessBase ):
    def __init__(self: Self):
        super(MainAppProc, self).__init__( "app-main" )
        self.keyval_schema: KeyValueSchema | None = None

    def init_internals( self: Self ) -> None:
        self.keyval_schema = BootLogSchema( id= "1", _log_root = "/home/richard/data/jctl-logs/" )
        self.msg_queue = MainAppMsgQueue()
        super().init_internals()

    def start(self: Self) -> bool:
        self.msg_queue.start()
        return True

class MainAppMsgQueue( MsgQueueBase ):
    def __init__(self: Self):
        super(MainAppMsgQueue, self).__init__( "app-main-msg-queue" )

    def recv_status( self: Self, msg: StatusMsg ) -> None:
        print(f"MainApp.StatusMsg: {msg}")

    def recv_info( self: Self, msg: InfoMsg ) -> None:
        print(f"MainApp.InfoMsg: {msg}")

    def recv_error( self: Self, msg: ErrorMsg ) -> None:
        print(f"MainApp.ErrorMsg: {msg}")

    def recv_data( self: Self, msg: DataMsg ) -> None:
        print(f"MainApp.DataMsg: {msg}")
