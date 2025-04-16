from typing import Self

import multiprocessing as mp
import threading as th

from .ProcLib import ProcRegistry

from . import ProcBase
from ..tasks.MsgRecvTask import MsgRecvTask

class AppProcessBase( ProcRegistry ):
    instance: Self | None = None

    def __init__(self: Self, app_id: str) -> None:
        super( AppProcessBase, self ).__init__()
        AppProcessBase.instance = self
        ProcRegistry.instance = self
        self.app_id: str = app_id
        self.procs: dict[str, ProcBase] = {}
        self.msg_queue: MsgRecvTask | None = None
        self.init_internals()

    def init_internals( self: Self ) -> None:
        pass

    def register_proc( self: Self, proc: ProcBase ) -> None:
        self.procs[proc.proc_id] = proc

    def start_proc( self, proc_id: str ):
        if proc_id in self.procs:
            self.procs[proc_id].start()
        else:
            #throw_error(f"[ProcManager.start_proc] Unknown Proc ID: {proc_id}")
            print(f"[ProcManager.start_proc] Unknown Proc ID: {proc_id}")

    async def start( self ):
        pass


