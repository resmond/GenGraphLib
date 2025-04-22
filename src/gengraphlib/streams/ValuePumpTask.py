from typing import Self

import multiprocessing as mp
import datetime as dt
import threading as th

from ..common import KeyRecordPacket, KeyValuePacket
from ..proc.TaskLib import TaskBase
from ..graph.KeySchemaVisitor import KeySchemaVisitor
from ..graph.KeyValueSchema import KeyValueSchema
from ..index.IndexManagerTask import IndexManagerTask

class ValuePumpTask( TaskBase, KeySchemaVisitor[bool] ):
    very_beginning = dt.datetime.fromisoformat("1970-01-01")

    def __init__( self: Self, keyvalue_schema: KeyValueSchema ) -> None:
        super( ValuePumpTask, self ).__init__( "value-pump" )

        self.keyvalue_schema: KeyValueSchema = keyvalue_schema
        self.indexmanager_task: IndexManagerTask | None = None
        self.queues_byalias: dict[str, mp.Queue] | None = None

        self.record_queue: mp.Queue = mp.Queue()
        self.thread = th.Thread(
            target=self.main_loop,
            name="ValuePumpTask",
            args=(self.record_queue, ),
        )

    # noinspection PyTypeChecker
    def init_queues( self: Self, indexmanager_task: IndexManagerTask ) -> mp.Queue:
        self.indexmanager_task = indexmanager_task
        self.queues_byalias = self.indexmanager_task.queues_byalias()
        return self.record_queue

    def start( self: Self ) -> None:
        if self.indexmanager_task is None:
            raise ValueError("ValuePumpTask not initialized with IndexManagerTask")

        self.thread.start()

    def main_loop( self: Self, record_queue: mp.Queue ) -> None:
        while True:
            record_packet: KeyRecordPacket = record_queue.get()
            if record_packet is not None:
                self.recv_valuemsgs( record_packet )
            else:
                break

    def recv_valuemsgs( self: Self, record_packet: KeyRecordPacket ) -> None:

        rec_num: int = record_packet[0]

        for keyvalue_pair in record_packet[1]:
            alias, value = keyvalue_pair
            keyindex_queue: mp.Queue = self.queues_byalias[ alias ]
            value_packet: KeyValuePacket = ( rec_num, value )
            keyindex_queue.put(value_packet)
