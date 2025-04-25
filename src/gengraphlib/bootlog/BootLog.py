from typing import Self

import os
import datetime as dt
import multiprocessing as mp

from ..streams import ValueIndexMsgPump
from .BootLogInfo import BootLogInfo

class BootLog:

    def __init__( self: Self, root_dir: str, logrec_line: str ) -> None:
        val_list: list[str] = logrec_line.split()
        self.root_dir = root_dir
        self.boot_index: int = int( val_list[0] )
        self.boot_id:    str = val_list[1]
        self.first_dt: dt.datetime = dt.datetime.fromisoformat(" ".join(val_list[3:5]))
        self.last_dt:  dt.datetime = dt.datetime.fromisoformat(" ".join(val_list[7:9]))
        self._boot_label:    str = self.boot_label()
        self.bootlog_path:   str = os.path.join( self.root_dir, "boots", self._boot_label )
        self.keys_path:      str = os.path.join( self.root_dir, "keys" )

        self.active_keys:          set[str] | None = None
        self.valuemux_queue:       mp.Queue | None = None
        self.journal_streamsource: ValueIndexMsgPump | None = None

    def boot_label( self: Self ) -> str:
        yymmdd: str = self.first_dt.strftime("%y-%m-%d")
        hhmm:   str = self.first_dt.strftime("%H-%M")
        return f"{yymmdd}:{hhmm}"

    def make_dir( self: Self ) -> bool:
        try:
            os.makedirs( self.bootlog_path, exist_ok=True )
            return True

        except Exception as e:
            print(f'[BootLog._dir_exists] Exception: {e}')
            return False

    def __repr__( self: Self ) -> str:
        return f'{{idx:{self.boot_index}, id:{self.boot_id}, first_dt:{self.first_dt}, last_dt:{self.last_dt}, dir_name:{self.boot_label}, dir_path:{self.bootlog_path}, keys_filepath:{self.keys_path}}}'

    def __str__( self: Self ) -> str: return self.__repr__()

    def get_info( self: Self ) -> BootLogInfo:
        return BootLogInfo(
            schema_bootid=self.boot_label(),
            boot_index=self.boot_index,
            first_dt=self.first_dt,
            last_dt=self.last_dt,
            dir_name=self._boot_label,
            dir_path=self.bootlog_path,
            keys_path=self.keys_path
        )

    def start_streaming( self, queues_byalias: dict[str, mp.Queue ], end_event: mp.Event, write_bin: bool = False, write_log: bool = False ):
        #self.active_keys = active_keys
        #self.valuemux_queue = valuemux_queue
        self.journal_streamsource = ValueIndexMsgPump( bootlog_info = self.get_info(), write_bin=write_bin, write_log = write_log )
        self.journal_streamsource.start_stream( queues_byalias, end_event )





