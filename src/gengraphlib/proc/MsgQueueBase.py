from abc import ABC
from typing import Self

import multiprocessing as mp

from .Messages import MessageBase, StatusMsg, ErrorMsg, InfoMsg, DataMsg


class MsgQueueBase( ABC ):

    def __init__(self: Self) -> None:
        self.msg_queue: mp.Queue[MessageBase] = mp.Queue(4096)

    async def start( self: Self ) -> None:
        await self.msg_loop()

    def send_msg( self: Self, msg: MessageBase ) -> None:
        self.msg_queue.put(msg)

    def recv_msg( self: Self ) -> MessageBase:
        return self.msg_queue.get()

    async def msg_loop( self: Self ) -> None:
        self.msg_queue = mp.SimpleQueue[MessageBase]()
        while True:
            incoming_message: MessageBase = self.msg_queue.get()
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
