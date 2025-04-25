import multiprocessing as mp
from typing import Any, Self

from PySide6.QtCore import QObject, QSocketNotifier, Signal

class QtMsgQueueReader( QObject ):
    activated     = Signal(object)
    data_received = Signal(object)

    def __init__(self: Self, msgqueue: mp.Queue, parent: QObject | None = None):
        super().__init__(parent)
        self.msgqueue: mp.Queue = msgqueue
        self.reader: Any | None = None

        self.reader, writer, rlock, wlock = self.msgqueue.__getstate__()

        self.notifier = QSocketNotifier(
            self.reader.fileno(),
            QSocketNotifier.Type.Read,
            self
        )
        #self.notifier.activate()

        # noinspection PyUnresolvedReferences
        self.notifier.activated.connect(self.read_from_queue)
        self.notifier.setEnabled(True)

    def read_from_queue(self: Self):
        while not self.msgqueue.empty():
            data = self.msgqueue.get()
            self.data_received.emit(data)

