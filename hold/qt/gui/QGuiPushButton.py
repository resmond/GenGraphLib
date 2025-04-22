from typing import Self, Any

from PySide6.QtCore import Signal, Property, Slot

from PySide6.QtWidgets import QPushButton

class QGuiPushButton( QPushButton ):

    def __init__( self: Self, objname: str = "" ) -> None:
        QPushButton.__init__(self)
        self.objectName = objname

    def keyPressEvent(self: Self, arg_1: Any, /) -> None:
        print(f"QGuiPushButton.keyPressEvent() arg_1 [{type(arg_1)}] = {arg_1}")




