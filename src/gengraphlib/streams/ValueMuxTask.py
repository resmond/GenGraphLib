from typing import Self

import multiprocessing as mp
import threading as th

from ..common import KeyRecordPacket, KeyValuePacket
from ..proc.TaskLib import TaskBase

class ValueMuxTask( TaskBase ):

    def __init__( self: Self, queues_byalias: dict[str, mp.Queue] ) -> None:
        super( ValueMuxTask, self ).__init__( "value-mux" )

        self.queues_byalias: dict[str, mp.Queue] = queues_byalias
        self.record_queue: mp.Queue = mp.Queue(maxsize=TaskBase.default_queue_size)
        self.thread = th.Thread(
            target=self.main_loop,
            name="value-mux-task",
            args=(self.record_queue, ),
        )

    # noinspection PyTypeChecker
    def get_queue( self: Self ) -> mp.Queue:
        return self.record_queue

    def start( self: Self ) -> None:
        self.thread.start()

    def stop( self: Self ) -> None:
        self.record_queue.put(None)
        self.thread.join()

    def main_loop( self: Self, record_queue: mp.Queue ) -> None:

        while True:

            record_packet: KeyRecordPacket = record_queue.get()
            if record_packet is None:
                break
            else:

                rec_num: int = record_packet[0]

                for keyvalue_pair in record_packet[1]:

                    alias, value = keyvalue_pair
                    value_packet: KeyValuePacket = (rec_num, value)

                    keyindex_queue: mp.Queue = self.queues_byalias[alias]
                    keyindex_queue.put(value_packet)
