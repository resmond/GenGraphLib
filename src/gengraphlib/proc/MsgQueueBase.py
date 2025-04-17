from typing import Self, Any

import multiprocessing as mp
import threading as th
import pickle as pkl

from .Messages import MessageBase, StatusMsg, ErrorMsg, InfoMsg, DataMsg, MsgType

class MsgQueueBase:

    def __init__(self: Self, queue_id ) -> None:
        self.queue_id: str = queue_id
        self.thread: th.Thread | None = None
        self.msg_queue: mp.Queue = mp.Queue(4096)

    def start( self: Self ) -> None:
        self.thread = th.Thread(target=self.msg_loop, args=())
        self.thread.start()

    def send_msg( self: Self, msg: MessageBase ) -> None:
        # msgtype_buf: bytes = msg.msg_type.value.to_bytes(4)
        # buffer: bytes = pkl.dumps(msg)
        # buffer = msgtype_buf + buffer
        self.msg_queue.put(msg)

    def recv_msg( self: Self ) -> MessageBase | None:
        msg: MessageBase = self.msg_queue.get()
        # msgtype: MsgType  = MsgType( int.from_bytes(buffer[0:3]) )
        # msg: MessageBase | None = None
        match MessageBase:
            case -1:
                msg: ErrorMsg = pkl.loads(buffer[3:])
            case 0:
                msg: StatusMsg = pkl.loads(buffer[3:])
            case 1:
                msg: InfoMsg = pkl.loads(buffer[3:])
            case 2:
                msg: DataMsg = pkl.loads(buffer[3:])

        return msg

    def msg_loop( self: Self ) -> None:
        print("[MsgQueBase.msg_loop] Started")
        while True:
            incoming_message = self.msg_queue.get()
            print("[MsgQueBase.msg_loop] Started")
            match incoming_message:
                case StatusMsg(status_msg):
                    self.recv_status( status_msg )
                case ErrorMsg(err_msg):
                    self.recv_error( err_msg )
                case InfoMsg(info_msg):
                    self.recv_info( info_msg )
                case DataMsg(data_msg):
                    self.recv_data( data_msg )

    def recv_status( self: Self, msg: StatusMsg ) -> None: ...
    def recv_error( self: Self, msg: ErrorMsg ) -> None: ...
    def recv_info( self: Self, msg: InfoMsg ) -> None: ...
    def recv_data( self: Self, msg: DataMsg ) -> None: ...


