from typing import Self, Any
from abc import ABC, abstractmethod

import multiprocessing as mp
import threading as th

from PySide6.QtCore import QSocketNotifier

from .Messages import MessageBase, StatusMsg, ErrorMsg, InfoMsg, DataMsg

class MsgQueueBase(ABC):

    def __init__(self: Self, queue_id, threaded: bool = True ) -> None:
        self.queue_id: str = queue_id
        self._inner_queue: mp.Queue = mp.Queue( 4096 )
        self.thread: th.Thread | None = None
        self.threaded: bool = threaded

        self.reader: Any | None = None

        self.reader, writer, rlock, wlock = self._inner_queue.__getstate__()

        self.notifier = QSocketNotifier(
            self.reader.fileno(), QSocketNotifier.Type.Read, self
        )

        # noinspection PyUnresolvedReferences
        self.notifier.activated.connect(self.read_from_queue)

        self.notifier.setEnabled(True)


    @property
    def inner_queue( self: Self ) -> mp.Queue:
        return self._inner_queue

    def start( self: Self ) -> None:
        if self.threaded:
            self.thread = th.Thread(target=self.msg_loop, args=() )
            self.thread.start()
        else:
            self.msg_loop()

    def send_msg( self: Self, msg: MessageBase ) -> None:
        self._inner_queue.put( msg )

    def msg_loop( self: Self ) -> None:
        #print("[MsgQueBase.msg_loop] Started")
        while True:
            incoming_message = self._inner_queue.get()
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


