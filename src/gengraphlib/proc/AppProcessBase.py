from multiprocessing.managers import SyncManager
from typing import Self

import multiprocessing as mp
import concurrent.futures as cf

from .ProcLib import ProcRegistry, Startable
from .MsgQueueBase import MsgQueueBase

class AppProcessBase( ProcRegistry ):
    instance: Self | None = None

    def __init__(self: Self, app_id: str) -> None:
        super( AppProcessBase, self ).__init__()
        AppProcessBase.instance = self
        self.app_id: str = app_id
        self.startables: dict[str, Startable ] = {}
        self.queuess: dict[str, mp.Queue ] = {}
        self.msg_queue: MsgQueueBase | None = None
        self.manager: SyncManager | None = mp.Manager()
        self.thread_exe: cf.ThreadPoolExecutor | None = cf.ThreadPoolExecutor(max_workers=4)
        self.init_internals()

    def init_internals( self: Self ) -> None:
        pass

    def create_queue( self: Self, queue_id: str ):
        queue: mp.Queue =  self.manager.Queue()
        self.queues[ queue_id ] = queue
        return queue

    def register_startable( self: Self, startable: Startable ) -> None:
        self.startables[ startable.id() ] = startable

    def start_proc( self: Self, proc_id: str ):
        if proc_id in self.startables:
            self.startables[proc_id ].start()
        else:
            #throw_error(f"[ProcManager.start_proc] Unknown Proc ID: {proc_id}")
            print(f"[ProcManager.start_proc] Unknown Proc ID: {proc_id}")

    def start( self: Self ):
        pass

    def stop( self: Self ):

        for proc in self.startables.values():
            if not proc.is_proc():
                proc.stop()


        #self.executor.shutdown()
        #self.manager.shutdown()


