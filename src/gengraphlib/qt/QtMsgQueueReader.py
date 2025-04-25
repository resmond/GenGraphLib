import multiprocessing as mp
import time
from typing import Any, Self

from PySide6.QtCore import QObject, Signal

class QtMsgQueueReader( QObject ):
    activated     = Signal(object)
    data_received = Signal(object)

    def __init__( self: Self, msg_queue: mp.Queue, end_event: mp.Event, parent: QObject | None = None ):
        super().__init__(parent)
        self.msg_queue: mp.Queue = msg_queue
        self.end_event: mp.Event = end_event

        self.reader_process = mp.Process(
            target=self._reader_process_func,
            args=(self.msg_queue, self.end_event,)   #, self.should_stop
        )
        # Set as daemon so it doesn't block program exit
        self.reader_process.daemon = True
        self.reader_process.start()

    def _reader_process_func( self: Self, queue: mp.Queue, end_event: mp.Event ):
        """Function that runs in the separate process"""
        try:
            while not end_event.is_set():
                try:
                    # Non-blocking queue check with timeout
                    if not queue.empty():
                        message = queue.get(block=False)
                        self._process_message(message)
                    time.sleep(0.01)  # Short sleep to prevent CPU hogging
                except Exception as e:
                    print(f"Error processing message: {e}")

        except KeyboardInterrupt:
            print("Reader received interrupt, shutting down gracefully")
        finally:
            print("Reader process exiting")

    def _process_message(self: Self, message):
        print(f"Processing message: {message}")
        self.data_received.emit(message)


        #self.reader, writer, rlock, wlock = self.msgqueue.__getstate__()
        # self.notifier = QSocketNotifier(
        #     self.reader.fileno(),
        #     QSocketNotifier.Type.Read,
        #     self
        # )
        #
        # # noinspection PyUnresolvedReferences
        # self.notifier.activated.connect(self.read_from_queue)
        # self.notifier.setEnabled(True)

    # def read_from_queue(self: Self):
    #     while not self.msg_queue.empty():
    #         data = self.msg_queue.get()
    #         self.data_received.emit(data)

