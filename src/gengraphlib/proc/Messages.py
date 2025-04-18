from enum import IntEnum
from typing import Self

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
        self.msg_type: MsgType = MsgType.Status
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

    def __init__(self: Self, source_id: str, message: str, data_dict: dict[str, str] | None = None):
        super(DataMsg, self).__init__(source_id, message)
        self.msg_type = MsgType.Data
        self.data: dict[str, str] = data_dict

if __name__ == "__main__":
    import multiprocessing as mp
    import pickle as pkl
    import asyncio as aio

    queue: mp.Queue = mp.Queue()

    def send_msg(msg: MessageBase):
        queue.put(msg)

    def recv_msg(buffer: bytes) -> MessageBase | None:
        msgtype: int = int.from_bytes(buffer[0:3])
        msg: MessageBase | None = None
        match msgtype:
            case MsgType.Error:
                msg: ErrorMsg = pkl.loads(buffer[3:])
            case MsgType.Status:
                msg: StatusMsg = pkl.loads(buffer[3:])
            case MsgType.Info:
                msg: InfoMsg = pkl.loads(buffer[3:])
            case MsgType.Data:
                msg: DataMsg = pkl.loads(buffer[3:])

        return msg

    def get_msg() -> None:
        buffer = queue.get()
        msg = recv_msg(buffer)
        print(msg)

    def test_proc():
        process = mp.Process(target=get_msg, args=())
        process.start()

    if __name__ == "__main__":
        test_proc()
        status_msg = StatusMsg("test-id", "test-msg")
        aio.sleep(3)
        send_msg(status_msg)
        aio.sleep(3)
        print(status_msg)
