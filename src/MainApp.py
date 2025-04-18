from typing import Self

from BootLogSchema import BootLogSchema
from gengraphlib import (
    StatusMsg,
    InfoMsg,
    ErrorMsg,
    DataMsg,
    MsgQueueBase,
    BootLogDir,
    JounalCtlStreamSource,
    AppProcessBase
)

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

class MainApp( AppProcessBase ):
    def __init__(self: Self):
        self.keyval_schema: BootLogSchema | None = None
        super( MainApp, self ).__init__( "app-main" )

    def init_internals( self: Self ) -> None:
        self.keyval_schema = BootLogSchema( id= "1", _log_root = "/home/richard/data/jctl-logs/" )
        self.msg_queue = MainAppMsgQueue()
        super().init_internals()

    def start(self: Self) -> bool:
        self.msg_queue.start()
        self.launch_processing()
        return True

    def launch_processing( self ):
        self.keyval_schema.launch_processing( -1, True )
