
from typing import Self


from PySide6.QtWidgets import QMainWindow, QWidget

from hold.qt.gui.QGuiLayoutHost import QGuiLayoutHost


class QGuiCentralWidget( QWidget, QGuiLayoutHost ):

    def __init__( self: Self, main_window: QMainWindow, objname: str = "" ) -> None:
        QWidget.__init__(self, main_window)
        self.objectName = objname
        self.main_window: QMainWindow = main_window
        self.main_window.setCentralWidget(self)
        self.wrappers: list[QWidget] | None = None






