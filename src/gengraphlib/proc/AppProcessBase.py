from multiprocessing.managers import SyncManager
from typing import Self

import multiprocessing as mp
import concurrent.futures as cf

from .ProcLib import ProcRegistry, Startable

class AppProcessBase( ProcRegistry ):
    instance: Self | None = None

    def __init__(self: Self, app_id: str) -> None:
        super( AppProcessBase, self ).__init__()
        AppProcessBase.instance = self

        self.app_id: str = app_id
        self.startables: dict[str,Startable] = {}
        self.queue_map: dict[str, mp.Queue] = {}
        self.sync_manager: SyncManager | None = mp.Manager()
        self._mainapp_msgqueue = self.sync_manager.Queue()
        self._end_event: mp.Event = self.sync_manager.Event()
        self.threadpool_ex: cf.ThreadPoolExecutor | None = cf.ThreadPoolExecutor( max_workers=4 )

    def init_internals( self: Self ) -> None:
        pass

    def mainapp_msgqueue( self: Self ) -> mp.Queue:
        return self._mainapp_msgqueue
    
    def end_event( self: Self ) -> mp.Event:
        return self._end_event

    def create_queue( self: Self, queue_id: str ) -> mp.Queue:
        self.queue_map[queue_id] = self.sync_manager.Queue()
        return self.queue_map[queue_id]

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


