from typing import Self, Dict, List, Any


from PySide6.QtCore import Signal, Property, Slot, QObject, QAbstractTableModel, QModelIndex

# noinspection PyPep8Naming
class QtGuiTreeModel( QObject, QAbstractTableModel, QModelIndex ):
    depthChanged      = Signal()
    isExpandedChanged = Signal()
    checkedChanged    = Signal()
    childrenChanged   = Signal()
    parentChanged     = Signal()
    dataChanged       = Signal()

    @Property(dict, notify=dataChanged)
    def data(self: Self) -> Dict[str, Any]:
        return self._data

    @data.setter
    def data(self: Self, value: Dict[str, Any]) -> None:
        self._data = value
        self.dataChanged.emit()

    @Slot(result=bool)
    def hasChildren(self: Self) -> bool:
        return len(self._children) != 0

    @Slot(int, result=bool)
    def hasNextNodeByIndex(self: Self, index: int) -> bool:
        p: Self = self
        for i in range(self._depth - index - 1):
            p: QObject = p._parent
        if p._parent._children.index(p) == len(p._parent._children) - 1:
            return False
        return True

    @Slot(result=bool)
    def hideLineFooter(self: Self) -> bool:
        if self._parent and self in self._parent._children:
            _pchildren = self._parent._children
            childIndex = _pchildren.index(self)
            if childIndex == len(_pchildren) - 1 or _pchildren[childIndex + 1].hasChildren():
                return True

        return False

    @Slot(result=bool)
    def isShown(self: Self) -> bool:
        p = self._parent
        while p is not None:
            if not p.isExpanded:
                return False
            p = p._parent
        return True

    @Property(int, notify=depthChanged)
    def depth(self: Self) -> int:
        return self._depth

    @depth.setter
    def depth(self: Self, value: int) -> None:
        self._depth = value
        self.depthChanged.emit()

    @Property(bool, notify=isExpandedChanged)
    def isExpanded(self: Self) -> bool:
        return self._isExpanded

    @isExpanded.setter
    def isExpanded(self: Self, value: bool) -> None:
        self._isExpanded = value
        self.isExpandedChanged.emit()

    @Property(bool, notify=checkedChanged)
    def checked(self: Self) -> bool:
        if not self.hasChildren():
            return self._checked
        for item in self._children:
            if not item.checked:
                return False
        return True

    @checked.setter
    def checked(self: Self, value: bool) -> None:
        self._checked = value
        self.checkedChanged.emit()

    @Property(QObject, notify=parentChanged)
    def parent_(self: Self) -> Self | None:
        return self._parent

    @parent_.setter
    def parent_(self: Self, value: Self | None) -> None:
        self._parent = value
        self.parentChanged.emit()

    @Property(list, notify=childrenChanged)
    def children_(self: Self) -> List[Self]:
        return self._children

    @children_.setter
    def children_(self: Self, value: List[Self]) -> None:
        self._children = value
        self.childrenChanged.emit()

    def __init__(self: Self, parent: QObject | None = None) -> None:
        QObject.__init__(self, parent)
        self._parent: Self | None = None
        self._data: Dict[str, Any] | None = None
        self._title: str = ""
        self._depth: int = 0
        self._isExpanded: bool = True
        self._checked: bool = False
        self._children: List[Self] = []