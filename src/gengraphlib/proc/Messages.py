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






