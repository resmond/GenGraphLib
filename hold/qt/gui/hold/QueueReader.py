from typing import Self

# import sys
# import signal
import multiprocessing as mp
import time


# noinspection DuplicatedCode
class QtMsgQueueReader:
    def __init__( self: Self, app_msgqueue: mp.Queue, end_event: mp.Event ) -> None:
        self.manager = mp.Manager()
        self.app_msgqueue: mp.Queue = app_msgqueue
        self.end_event: mp.Event    = end_event
        self.reader_process = None

    def start_reader( self: Self ) -> None:
        if self.reader_process is not None and self.reader_process.is_alive():
            print("Reader process already running")
            return

        self.reader_process = mp.Process(
            target=self._reader_loop,
            args=(self.app_msgqueue, self.end_event,)
        )

        self.reader_process.daemon = True
        self.reader_process.start()
        print(f"Started reader process with PID {self.reader_process.pid}")

    def _reader_loop(self, queue: mp.Queue, stop_event: mp.Event):

        try:
            while not stop_event.is_set():
                try:

                    if not queue.empty():
                        message = queue.get(block=False)
                        self._process_message(message)

                    time.sleep(0.01)

                except Exception as e:
                    print(f"Error processing message: {e}")

        except KeyboardInterrupt:
            print("Reader received interrupt, shutting down gracefully")

        finally:
            print("Reader process exiting")

    def _process_message(self, message):
        print(f"{self}:  Processing message: {message}")

    def stop(self):
        if self.reader_process and self.reader_process.is_alive():
            print("Stopping reader process...")
            self.end_event.set()
            self.reader_process.join(timeout=2.0)

            # If process is still alive after timeout, terminate it
            if self.reader_process.is_alive():
                print("Reader process did not terminate gracefully, forcing termination")
                self.reader_process.terminate()
                self.reader_process.join(timeout=1.0)

            print("Reader process stopped")

# Example usage
def main():
    app_msgqueue: mp.Queue = mp.Queue()
    end_event:    mp.Event = mp.Event()

    # Set up signal handling
    # def signal_handler(sig, frame):
    #     print("Received interrupt signal, shutting down...")
    #     if reader:
    #         reader.stop()
    #     sys.exit(0)
    #
    # signal.signal(signal.SIGINT, signal_handler)

    reader = QtMsgQueueReader(app_msgqueue,end_event)
    reader.start_reader()



