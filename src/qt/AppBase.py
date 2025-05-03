from multiprocessing.managers import SyncManager
from typing import Self


import multiprocessing as mp
import concurrent.futures as cf

class AppBase:
    instance: Self | None = None

    def __init__(self: Self, app_id: str) -> None:
        super().__init__()
        AppBase.instance = self

        self.app_id: str = app_id
        self._queue_map:  dict[str, mp.Queue ] = {}
        self._sync_manager: SyncManager | None = mp.Manager()
        self._app_msgqueue = self._sync_manager.Queue()
        self._end_event: mp.Event = self._sync_manager.Event()
        self._threadpool_ex: cf.ThreadPoolExecutor | None = cf.ThreadPoolExecutor( max_workers=4 )

    def app_msgqueue( self: Self ) -> mp.Queue:
        return self._app_msgqueue
    
    def end_event( self: Self ) -> mp.Event:
        return self._end_event



