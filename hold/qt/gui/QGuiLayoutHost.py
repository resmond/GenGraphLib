from types import UnionType

from typing import Self, overload, Iterable, Any

from abc import ABC

from PySide6.QtWidgets import QGraphicsLayout, QGraphicsLayoutItem, QWidget

MultiTup: type = tuple[...,Any]

TupList: type = Iterable[MultiTup]

LoopyTup: UnionType = MultiTup | TupList | QGraphicsLayoutItem



class QGuiLayoutHost( QGraphicsLayout, ABC ):

    def __add__( self: Self, new_children: LoopyTup ) -> Self:
        match new_children:
            case QGraphicsLayoutItem() as item:
                item.setParentLayoutItem(self)
                self.addChildLayoutItem(item)
            case TupList() as tlist:
                for tup in tlist:
                    self + tup
            case MultiTup() as mlist:
                for tup in mlist:
                    self + tup

        return self


    # def __add__(self: Self, new_child: QGraphicsLayoutItem ) -> Self:
    #     if new_child not in self.children():
    #         new_child.setParentLayoutItem(self)
    #         self.addChildLayoutItem(new_child)
    #
    #     return self



