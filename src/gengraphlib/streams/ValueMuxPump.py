from typing import Self

import multiprocessing as mp
import datetime as dt

from ..common import KeyType, KeyRecordPacket
from ..proc.TaskLib import TaskBase
from ..graph.KeySchemaVisitor import KeySchemaVisitor
from ..graph.KeyValueSchema import KeyValueSchema
from .IndexManagerTask import IndexManagerTask

class ValuePumpTask( TaskBase, KeySchemaVisitor[bool] ):
    very_beginning = dt.datetime.fromisoformat("1970-01-01")

    def __init__( self: Self, keyvalue_schema: KeyValueSchema ) -> None:
        super( ValuePumpTask, self ).__init__( "value-pump" )
        self.keyvalue_schema: KeyValueSchema = keyvalue_schema
        self.indexmanager_task: IndexManagerTask | None = None
        self.record_queue: mp.Queue[KeyRecordPacket] = mp.Queue[KeyRecordPacket]()

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

        for value in record_packet[1]:
            alias, buffer = value

            keyindex_queue: mp.Queue = self.queues_byalias[ alias ]

            match self.key_def.keytype:
                case KeyType.KStr:
                    keyindex_queue.put( value )

                case KeyType.KInt:
                    keyindex_queue.put( value )

                case KeyType.KBool:
                    keyindex_queue.put( value )

                case KeyType.KFloat:
                    keyindex_queue.put( value )

                case KeyType.KTmst:
                    keyindex_queue.put( value )

                case _:
                    print(f"ValuePumpTask.send_valuemsgs - rec_num: {rec_num}  key: {alias} value: {value}")

    # from ..graph.KeyDefs import (
    #     KeyDefBase,
    #     StrKeyDef,
    #     IntKeyDef,
    #     BoolKeyDef,
    #     FloatKeyDef,
    #     TmstKeyDef,
    # )
    # from ..graph.KeyValues import (
    #     StrKeyValueSet,
    #     IntKeyValueSet,
    #     BoolKeyValueSet,
    #     FloatKeyValueSet,
    #     TmstKeyValueSet,
    # )

    # def visit_str( self: Self, keydef: StrKeyDef, keyvalues: StrKeyValueSet ) -> bool:
    #     return self.register_queue( keydef )
    #
    # def visit_int( self: Self, keydef: IntKeyDef, keyvalues: IntKeyValueSet ) -> bool:
    #     return self.register_queue( keydef )
    #
    # def visit_bool( self: Self, keydef: BoolKeyDef, keyvalues: BoolKeyValueSet ) -> bool:
    #     return self.register_queue( keydef )
    #
    # def visit_float( self: Self, keydef: FloatKeyDef, keyvalues: FloatKeyValueSet ) -> bool:
    #     return self.register_queue( keydef )
    #
    # def visit_tmst( self: Self, keydef: TmstKeyDef, keyvalues: TmstKeyValueSet ) -> bool:
    #     return self.register_queue( keydef )
    #
    # def send_msg( self: Self, record_message: RecordDataMsg ) -> None:
    #     self.msg_queue.put( record_message )
    #
    # def main_loop(self: Self) -> None:
    #     while True:
    #         record_msg: RecordDataMsg = self.record_queue.get()
    #         self.send_valuemsgs( record_msg )
