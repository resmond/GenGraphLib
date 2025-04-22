from typing import Self

import multiprocessing as mp

from BootLogSchema import BootLogSchema, ParseProcessInfo
from gengraphlib import (
    StatusMsg,
    InfoMsg,
    ErrorMsg,
    DataMsg,
    MsgQueueBase,
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
        super( MainApp, self ).__init__( "app-main" )
        self.parse_info: ParseProcessInfo | None = None
        self.process: mp.Process | None = None

    def init_internals( self: Self ) -> None:
        self.msg_queue = MainAppMsgQueue()
        super().init_internals()

    def start(self: Self) -> bool:
        self.msg_queue.start()

        self.parse_info: ParseProcessInfo = \
            ParseProcessInfo(
                app_msgqueue=self.msg_queue.inner_queue,
                id="parse-proc",
                log_root= "/home/richard/data/jctl-logs/",
                boot_index = -1,
                write_bin = False,
                write_log = True
            )

        self.process: mp.Process = mp.Process( target = BootLogSchema.entrypoint, args=(self.parse_info,) )
        self.process.start()

        return True

