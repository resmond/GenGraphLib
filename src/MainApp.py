from typing import Self

import multiprocessing as mp

from PySide6.QtWidgets import QApplication


from gengraphlib import AppProcessBase

from BootLogSchema import BootLogSchema, ParseProcessInfo
from MyMainWin import MyMainWindow

class MainApp( AppProcessBase ):
    def __init__(self: Self):
        super( MainApp, self ).__init__( "app-main" )
        self.msg_queue: mp.Queue = mp.Queue()
        self.parse_info: ParseProcessInfo | None = None
        self.parse_process: mp.Process | None = None
        self.qt_app: QApplication = QApplication()
        self.main_window: MyMainWindow = MyMainWindow( self.msg_queue )
        self.main_window.setWindowTitle( "Boot Log Parser" )

    def init_internals( self: Self ) -> None:
        super().init_internals()

    def start(self: Self) -> bool:

        self.parse_info: ParseProcessInfo = \
            ParseProcessInfo(
                app_msgqueue=self.msg_queue,
                id="parse-proc",
                log_root= "/home/richard/data/jctl-logs/",
                boot_index = -1,
                groupid = "evt",
                write_log = True,
                autostart = True
            )

        self.parse_process: mp.Process = mp.Process( target = BootLogSchema.entrypoint, args=(self.parse_info,) )
        self.parse_process.start()

        self.main_window.show()
        self.qt_app.setActiveWindow( self.main_window )
        self.qt_app.exec()

        return True

