from typing import Self

import multiprocessing as mp
import threading as th

from ..common import KeyRecordPacket, KeyValuePacket
from ..proc.TaskLib import TaskBase

class ValueMuxPumpTask( TaskBase ):

    def __init__( self: Self ) -> None:
        super( ValueMuxPumpTask, self ).__init__( "value-mux" )
        self.thread: th.Thread | None = None

        self.record_queue: mp.Queue = mp.Queue(maxsize=TaskBase.default_queue_size)

    # noinspection PyTypeChecker
    def start_muxpump( self: Self, queues_byalias: dict[str, mp.Queue ] ) -> mp.Queue:

        self.thread = th.Thread(
            target  = ValueMuxPumpTask.main_loop,
            name    = "value-mux-task",
            args    = ( self.record_queue, queues_byalias, ),
        )

        self.thread.start()

        return self.record_queue

    # def start( self: Self ) -> None:
    #     self.thread.start()

    def stop( self: Self ) -> None:
        self.record_queue.put(None)
        self.thread.join()

    @staticmethod
    def main_loop( record_queue: mp.Queue, queues_byalias: dict[str, mp.Queue ] ) -> None:

        while True:

            record_packet: KeyRecordPacket = record_queue.get()
            if record_packet is None:
                break

            rec_num: int = record_packet[0]

            for keyvalue_pair in record_packet[1]:

                alias, value = keyvalue_pair
                value_packet: KeyValuePacket = (rec_num, value)

                keyindex_queue: mp.Queue = queues_byalias[alias]
                keyindex_queue.put(value_packet)
