from typing import Self

import os
import datetime as dt
import multiprocessing as mp

from ..common import KeyValSchemaInfo, BootLogInfo

from ..index.LogIndexingProcess import LogIndexingProcess
from ..columns import GraphTable


class BootLog:

    def __init__(
        self: Self,
        root_dir: str,
        logrec_line: str,
        schema_info: KeyValSchemaInfo,
        app_msgqueue: mp.Queue,
        end_event: mp.Event,
    ) -> None:
        self.root_dir = root_dir

        self.schema_info: KeyValSchemaInfo = schema_info
        self.app_msgqueue: mp.Queue        = app_msgqueue
        self.end_event: mp.Event           = end_event

        val_list: list[str] = logrec_line.split()
        self.boot_index: int = int( val_list[0] )
        self.boot_id:    str = val_list[1]
        self.first_dt: dt.datetime = dt.datetime.fromisoformat(" ".join(val_list[3:5]))
        self.last_dt:  dt.datetime = dt.datetime.fromisoformat(" ".join(val_list[7:9]))
        self.bootlog_path:   str = os.path.join( self.root_dir, "boots", str(self.boot_label()) )
        self.keys_path:      str = os.path.join( self.root_dir, "keys" )

        self.indexing_process: LogIndexingProcess | None = None
        self.graph_table:      GraphTable         | None = None
        self.active_keys:      set[str]           | None = None

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
        return f'{{idx:{self.boot_index}, id:{self.boot_id}, first_dt:{self.first_dt}, last_dt:{self.last_dt}, dir_name:{self.boot_label()}, dir_path:{self.bootlog_path}, keys_filepath:{self.keys_path}}}'

    def __str__( self: Self ) -> str: return self.__repr__()

    def get_info( self: Self ) -> BootLogInfo:
        return BootLogInfo(
            schema_bootid=str(self.boot_label),
            boot_index=self.boot_index,
            first_dt=self.first_dt,
            last_dt=self.last_dt,
            dir_name=self.boot_label(),
            dir_path=self.bootlog_path,
            keys_path=self.keys_path
        )

    def launch_indexing( self: Self, active_keys: set[str], write_bin: bool = False, write_log: bool = False ) -> GraphTable:
        self.indexing_process = LogIndexingProcess( self.schema_info, self.app_msgqueue, self.end_event )
        self.graph_table = GraphTable( "logevents", self.bootlog_path, self.schema_info.keys )
        self.graph_table.save_info()
        if self.indexing_process:
            self.indexing_process.index_bootlog( self.get_info(), self.graph_table, active_keys, write_bin, write_log )
        return self.graph_table




