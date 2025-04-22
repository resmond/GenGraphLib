from typing import Self

from PySide6.QtWidgets import QGraphicsLayout, QHBoxLayout

from .QGuiLayoutHost import QGuiLayoutHost

class QGuiHorzLayout( QHBoxLayout, QGuiLayoutHost ):

    def __init__( self: Self, objname: str = "" ) -> None:

        QHBoxLayout.__init__(self)
        self.objectName = objname




