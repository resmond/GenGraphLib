from typing import Self

import multiprocessing as mp
import datetime as dt

from ..common import KeyType
from ..proc.TaskLib import TaskBase
from ..graph.KeySchemaVisitor import KeySchemaVisitor
from ..graph.GraphMessages import RecordDataMsg, ValueDataMsg
from ..graph.KeyDefs import KeyDefBase, StrKeyDef, IntKeyDef, BoolKeyDef, FloatKeyDef, TmstKeyDef
from ..graph.KeyValues import StrKeyValueSet, IntKeyValueSet, BoolKeyValueSet, FloatKeyValueSet, TmstKeyValueSet
from ..graph.KeyValueSchema import KeyValueSchema

class ValuePumpTask( TaskBase, KeySchemaVisitor[bool] ):
    very_beginning = dt.datetime.fromisoformat("1970-01-01")

    def __init__( self: Self ) -> None:
        super( ValuePumpTask, self ).__init__( "value-pump" )
        self.data_msgqueue: mp.Queue = mp.Queue()

        self.keydef_queues: dict[str, mp.Queue] = dict[str, mp.Queue]()

    def init_queues( self: Self ) -> None:
        KeyValueSchema.schema.visit_schema( self )

    def register_queue( self: Self, key_def: KeyDefBase ) -> bool:
        if "evt" in key_def.groupids:
            self.keydef_queues[ key_def.alias ] = key_def.queue
        return True

    def visit_str( self: Self, keydef: StrKeyDef, keyvalues: StrKeyValueSet ) -> bool:
        return self.register_queue( keydef )

    def visit_int( self: Self, keydef: IntKeyDef, keyvalues: IntKeyValueSet ) -> bool:
        return self.register_queue( keydef )

    def visit_bool( self: Self, keydef: BoolKeyDef, keyvalues: BoolKeyValueSet ) -> bool:
        return self.register_queue( keydef )

    def visit_float( self: Self, keydef: FloatKeyDef, keyvalues: FloatKeyValueSet ) -> bool:
        return self.register_queue( keydef )

    def visit_tmst( self: Self, keydef: TmstKeyDef, keyvalues: TmstKeyValueSet ) -> bool:
        return self.register_queue( keydef )

    def send_msg( self: Self, record_message: RecordDataMsg ) -> None:
        self.msg_queue.put( record_message )

    def main_loop(self: Self) -> None:
        while True:
            record_msg: RecordDataMsg = self.data_msgqueue.get()
            self.send_valuemsgs( record_msg )

    def send_valuemsgs( self: Self, record_msg: RecordDataMsg ) -> None:

        rec_num: int = record_msg.rec_num

        for value in record_msg.values:
            key, buffer = value

            keyindex_queue: mp.Queue = self.keydef_queues[ key ]

            match self.key_def.keytype:
                case KeyType.KStr:
                    value_str: str = buffer.decode()
                    keyvalue_msg: ValueDataMsg = ValueDataMsg[str ]( "value-pump", rec_num, key, value_str )
                    keyindex_queue.put( keyvalue_msg )

                case KeyType.KInt:
                    value_int: int = int(buffer)
                    keyvalue_msg: ValueDataMsg = ValueDataMsg[int ]( "value-pump", rec_num, key, value_int )
                    keyindex_queue.put( keyvalue_msg )

                case KeyType.KBool:
                    value_bool: bool = bool( buffer )
                    keyvalue_msg: ValueDataMsg = ValueDataMsg[bool ]( "value-pump", rec_num, key, value_bool )
                    keyindex_queue.put( keyvalue_msg )

                case KeyType.KFloat:
                    value_float: float = float( buffer )
                    keyvalue_msg: ValueDataMsg = ValueDataMsg[float ]( "value-pump", rec_num, key, value_float )
                    keyindex_queue.put( keyvalue_msg )

                case KeyType.KTmst:
                    value_int: int = int(buffer)
                    value_dt: dt.datetime = self.very_beginning + dt.timedelta( microseconds=value_int )
                    keyvalue_msg: ValueDataMsg = ValueDataMsg[dt.datetime ]( "value-pump", rec_num, key, value_dt )
                    keyindex_queue.put( keyvalue_msg )

                case _:
                    print(f"ValuePumpTask.send_valuemsgs - rec_num: {rec_num}  key: {key} buffer: {buffer}")


