from typing import Self

import multiprocessing as mp
import datetime as dt

from ..common import KeyRecordPacket, KeyValuePacket
from ..proc.TaskLib import TaskBase
from ..graph.KeySchemaVisitor import KeySchemaVisitor
from ..graph.KeyValueSchema import KeyValueSchema
from src.gengraphlib.index.IndexManagerTask import IndexManagerTask

class ValuePumpTask( TaskBase, KeySchemaVisitor[bool] ):
    very_beginning = dt.datetime.fromisoformat("1970-01-01")

    def __init__( self: Self, keyvalue_schema: KeyValueSchema ) -> None:
        super( ValuePumpTask, self ).__init__( "value-pump" )
        self.keyvalue_schema: KeyValueSchema = keyvalue_schema
        self.indexmanager_task: IndexManagerTask | None = None
        self.record_queue: mp.Queue = mp.Queue()
        self.queues_byalias: dict[str, mp.Queue] | None = None

    # noinspection PyTypeChecker
    def init_queues( self: Self, indexmanager_task: IndexManagerTask ) -> mp.Queue:
        self.indexmanager_task = indexmanager_task
        self.queues_byalias = self.indexmanager_task.queues_byalias()
        return self.record_queue

    def start(self: Self) -> None:
        super().start()

    def main_loop( self ) -> None:
        pass

    def send_valuemsgs( self: Self, record_packet: KeyRecordPacket ) -> None:

        rec_num: int = record_packet[0]

        for keyvalue_pair in record_packet[1]:
            alias, value = keyvalue_pair
            keyindex_queue: mp.Queue = self.queues_byalias[ alias ]

            value_packet: KeyValuePacket = ( rec_num, value )

            keyindex_queue.put(value_packet)

            # match self.key_def.keytype:
            #     case KeyType.KStr:
            #         keyindex_queue.put( value )
            #
            #     case KeyType.KInt:
            #         keyindex_queue.put( value )
            #
            #     case KeyType.KBool:
            #         keyindex_queue.put( value )
            #
            #     case KeyType.KFloat:
            #         keyindex_queue.put( value )
            #
            #     case KeyType.KTmst:
            #         keyindex_queue.put( value )
            #
            #     case _:
            #         print(f"ValuePumpTask.send_valuemsgs - rec_num: {rec_num}  key: {alias} value: {value}")

