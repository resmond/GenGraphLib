from typing import Self

import os
import datetime as dt
import multiprocessing as mp

from ..streams import StreamSourceTask
from .BootLogInfo import BootLogInfo

class BootLog:

    def __init__( self: Self, root_dir: str, log_rec: str ) -> None:
        super( BootLog, self ).__init__()
        val_list: list[str] = log_rec.split()
        self.root_dir = root_dir
        self.index: int = int( val_list[0 ] )
        self.id: str = val_list[1]
        self.first_dt: dt.datetime = dt.datetime.fromisoformat(" ".join(val_list[3:5]))
        self.last_dt: dt.datetime = dt.datetime.fromisoformat(" ".join(val_list[7:9]))
        self.dir_name: str = self.boot_id()
        self.dir_path: str = os.path.join(self.root_dir, "boots", self.dir_name)
        self.keys_path: str = os.path.join( self.root_dir, "keys" )
        self.journal_streamsource: StreamSourceTask | None = None
        self.active_keys:  set[str] | None = None
        self.record_queue: mp.Queue | None = None

    def boot_id( self: Self ) -> str:
        yymmdd: str = self.first_dt.strftime("%y-%m-%d")
        hhmm: str   = self.first_dt.strftime("%H-%M")
        return f"{yymmdd}:{hhmm}"

    def make_dir( self: Self ) -> bool:
        try:
            os.makedirs( self.dir_path, exist_ok=True )
            return True

        except Exception as e:
            print(f'[BootLog._dir_exists] Exception: {e}')
            return False

    def __repr__( self: Self ) -> str:
        return f'{{idx:{self.index}, id:{self.id}, first_dt:{self.first_dt}, last_dt:{self.last_dt}, dir_name:{self.dir_name}, dir_path:{self.dir_path}, keys_filepath:{self.keys_path}}}'

    def __str__( self: Self ) -> str: return self.__repr__()

    def get_info( self: Self ) -> BootLogInfo:
        return BootLogInfo(
            schema_bootid=self.boot_id(),
            boot_index=self.boot_index,
            first_dt=self.first_dt,
            last_dt=self.last_dt,
            dir_name=self.dir_name,
            dir_path=self.dir_path,
            keys_path=self.keys_path
        )


    def start_streaming( self, record_queue: mp.Queue, active_keys: set[str], write_bin: bool = False, write_log: bool = False ):
        self.active_keys = active_keys
        self.record_queue = record_queue
        self.journal_streamsource = StreamSourceTask( bootlog_info = self.get_info(), write_bin=write_bin, write_log = write_log )
        self.journal_streamsource.start_stream( active_keys=self.active_keys, record_queue=self.record_queue )





