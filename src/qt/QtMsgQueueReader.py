import multiprocessing as mp
import time
from typing import Self

from PySide6.QtCore import QObject, Signal

from src.gengraphlib.common import IndexInfo

# noinspection DuplicatedCode
class QtMsgQueueReader( QObject ):
    activated     = Signal(object)
    data_received = Signal(object)

    def __init__( self: Self, msg_queue: mp.Queue, parent: QObject | None = None ):
        super().__init__(parent)
        self.msg_queue: mp.Queue = msg_queue

        self.reader_process = mp.Process(
            target=self._reader_process_func,
            args=(self.msg_queue, )
        )
        self.reader_process.daemon = True
        self.reader_process.start()

    def _reader_process_func( self: Self, queue: mp.Queue ):
        try:
            while True:
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

    def _process_message( self: Self, index_info: IndexInfo ):
        #print(f"Processing message: {index_info}")
        self.data_received.emit(index_info)
