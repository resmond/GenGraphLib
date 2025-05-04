from typing import Self

import multiprocessing as mp

from PySide6.QtWidgets import QApplication

from src.qt import AppBase

from MyMainWindow import MyMainWindow
from LogParseProcess import LogParseProcess, ParseProcessInfo

class MyMainApp( AppBase ):
    def __init__(self: Self):
        super().__init__( "app-main" )

        self.parse_info: ParseProcessInfo | None = None
        self.parse_process: mp.Process | None = None
        self.qt_app: QApplication = QApplication()
        self.main_window: MyMainWindow = MyMainWindow( self.app_msgqueue(), self.end_event() )
        self.main_window.setWindowTitle( "Boot Log Parser" )

    def start(self: Self) -> bool:

        self.parse_info: ParseProcessInfo = \
            ParseProcessInfo(
                app_msgqueue=self.app_msgqueue(),
                log_root= "/home/richard/data/jctl-logs/",
                boot_index = -1
            )

        self.parse_process: mp.Process = mp.Process( target = LogParseProcess.entrypoint, args=(self.parse_info,) )
        self.parse_process.start()

        self.main_window.show()
        self.qt_app.setActiveWindow( self.main_window )
        self.qt_app.exec()

        return True

