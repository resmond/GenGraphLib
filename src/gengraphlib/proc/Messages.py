from abc import ABC
from enum import IntEnum
from typing import Self

import multiprocessing as mp

class MsgType( IntEnum ):
    Error  = -1
    Status =  0
    Info   =  1
    Data   =  2

class MsgSourceType(IntEnum):
    Task = 0
    Proc = 1

class MessageBase:

    def __init__( self: Self, source_id: str, message: str, source_type: MsgSourceType = MsgSourceType.Task ):
        super(MessageBase, self).__init__()
        self.msg_type: MsgType
        self.source_type: MsgSourceType = source_type
        self.source_id: str = source_id
        self.message: str = message

class StatusMsg(MessageBase):

    def __init__(self: Self, source_id: str,  message: str, *kwargs):
        super(StatusMsg, self).__init__(source_id, message, kwargs )
        self.msg_type = MsgType.Status

class ErrorMsg(MessageBase):

    def __init__(self: Self, source_id: str,  message: str, *kwargs):
        super(ErrorMsg, self).__init__(source_id, message, kwargs )
        self.msg_type = MsgType.Error

class InfoMsg(MessageBase):

    def __init__(self: Self, source_id: str, message: str, *kwargs):
        super(InfoMsg, self).__init__(source_id, message, kwargs)
        self.msg_type = MsgType.Info

class DataMsg(MessageBase):

    def __init__(self: Self, source_id: str, message: str, *kwargs):
        super(DataMsg, self).__init__(source_id, message, kwargs)
        self.msg_type = MsgType.Data

class MessageQueueBase(ABC):

    def __init__(self: Self) -> None:
        self.msg_queue: mp.Queue[MessageBase] = mp.Queue(4096)

    def msg_loop( self: Self ) -> None:
        self.msg_queue = mp.SimpleQueue[MessageBase]()
        while True:
            incoming_message: MessageBase = self.recv_msg()
            match incoming_message:
                case StatusMsg(status_msg):
                    self.recvmsg_status(status_msg)
                case ErrorMsg(err_msg):
                    self.recvmsg_error(err_msg)
                case InfoMsg(info_msg):
                    self.recvmsg_info(info_msg)
                case DataMsg(data_msg):
                    self.recvmsg_data(data_msg)


    def send_msg( self: Self, msg: MessageBase ) -> None:
        self.msg_queue.put(msg)

    def recv_msg( self: Self ) -> MessageBase:
        return self.msg_queue.get()

    def recvmsg_status( self: Self, msg: StatusMsg ) -> None: ...
    def recvmsg_error( self: Self, msg: ErrorMsg ) -> None: ...
    def recvmsg_info( self: Self, msg: InfoMsg ) -> None: ...
    def recvmsg_data( self: Self, msg: DataMsg ) -> None: ...





