from typing import Self
from abc import ABC, abstractmethod

import multiprocessing as mp
import threading as th

from .Messages import MessageBase, StatusMsg, ErrorMsg, InfoMsg, DataMsg

class MsgQueueBase(ABC):

    def __init__(self: Self, queue_id, threaded: bool = True ) -> None:
        self.queue_id: str = queue_id
        self.msg_queue: mp.Queue = mp.Queue(4096)
        self.thread: th.Thread | None = None
        self.threaded: bool = threaded

    def start( self: Self ) -> None:
        if self.threaded:
            self.thread = th.Thread(target=self.msg_loop, args=() )
            self.thread.start()
        else:
            self.msg_loop()

    def send_msg( self: Self, msg: MessageBase ) -> None:
        self.msg_queue.put(msg)

    def msg_loop( self: Self ) -> None:
        #print("[MsgQueBase.msg_loop] Started")
        while True:
            incoming_message = self.msg_queue.get()
            #print("[MsgQueBase.msg_loop] Started")
            match incoming_message:
                case StatusMsg(status_msg):
                    self.recv_status( status_msg )
                case ErrorMsg(err_msg):
                    self.recv_error( err_msg )
                case InfoMsg(info_msg):
                    self.recv_info( info_msg )
                case DataMsg(data_msg):
                    self.recv_data( data_msg )

    @abstractmethod
    def recv_status( self: Self, msg: StatusMsg ) -> None: ...

    @abstractmethod
    def recv_error( self: Self, msg: ErrorMsg ) -> None: ...

    @abstractmethod
    def recv_info( self: Self, msg: InfoMsg ) -> None: ...

    @abstractmethod
    def recv_data( self: Self, msg: DataMsg ) -> None: ...


