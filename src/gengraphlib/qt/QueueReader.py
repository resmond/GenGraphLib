from typing import Self

import sys
import signal
import multiprocessing as mp
import time

class QtMsgQueueReader:
    def __init__( self: Self, app_msgqueue: mp.Queue, evt_stop: mp.Event ) -> None:
        self.manager = mp.Manager()
        self.message_queue = self.manager.Queue()
        self.should_stop   = self.manager.Event()
        self.reader_process = None

    def start_reader( self: Self ) -> None:
        if self.reader_process is not None and self.reader_process.is_alive():
            print("Reader process already running")
            return

        self.reader_process = mp.Process(
            target=self._reader_loop,
            args=(self.message_queue, self.should_stop, )
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
        print(f"Processing message: {message}")

    def stop(self):
        if self.reader_process and self.reader_process.is_alive():
            print("Stopping reader process...")
            self.should_stop.set()
            self.reader_process.join(timeout=2.0)

            # If process is still alive after timeout, terminate it
            if self.reader_process.is_alive():
                print("Reader process did not terminate gracefully, forcing termination")
                self.reader_process.terminate()
                self.reader_process.join(timeout=1.0)

            print("Reader process stopped")

# Example usage
def main():
    # Set up signal handling
    def signal_handler(sig, frame):
        print("Received interrupt signal, shutting down...")
        if reader:
            reader.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    reader = QtMsgQueueReader()
    reader.start_reader()

    try:
        # Example: add some messages
        for i in range(5):
            reader.add_message(f"Test message {i}")
            time.sleep(1)

        # Wait a bit before stopping
        time.sleep(2)
    finally:
        # Ensure we clean up properly
        reader.stop()

if __name__ == "__main__":
    main()

