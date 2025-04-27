from typing import Self

import subprocess
import datetime as dt
import os as os
import multiprocessing as mp

from .. import KeyValSchemaInfo

from .BootLog import BootLog


"""--------------------------------------------------------
    LogDirManagerBase __init__()
        root_dir - root of all log data
            root_dir/boots/{fulldate}/ files - being primary log data for a single boot history
            root_dir/keys - being primary key stats data for ALL boots
    
        self.root_dir = rot_dir
        self._cmd - last command executed
        self._bootlist_txtfilepath - path to "bootlist.txt" from 'journalctl --list-boots'
        self._bootrec_jfilepath: str = path to "bootlist.jline" json line data of --list-boots
        self._bootrec_list: list[BootRecord ] = tuple data for basic boot history entries
        self._bootdir_dict: dict[ dt.datetime, BootLogDir ] = dict of BootLogDir boot manager objects
        self._journal_cmd = "journalctl -b 0 -o json" = basic journalctl command for a single boot export to json


--------------------------------------------------------"""

class BootLogManager:

    def __init__(
        self: Self,
        root_dir: str,
        schema_info: KeyValSchemaInfo,
        app_msgqueue: mp.Queue,
        end_event: mp.Event,
    ) -> None:
        self.root_dir: str = root_dir
        self.schema_info: KeyValSchemaInfo = schema_info
        self.app_msgqueue: mp.Queue = app_msgqueue
        self.end_event: mp.Event = end_event

        self._bootdir_path: str = os.path.join( self.root_dir, "boots" )
        self._bootlist_txtfilepath: str = os.path.join( self.root_dir, "boots", "bootlist.txt" )
        self._bootlog_list: list[BootLog] = list[BootLog]()
        self._logdate_map: dict[dt.datetime, BootLog] = {}
        self._bootlog_index: dict[int, BootLog] = {}
        self._journal_cmd = f"/bin/journalctl --list-boots > {self._bootlist_txtfilepath}"

    """
        _log_querylist
            fqueries fresh list of boot records from journalctl --list-boots as text file
    """
    def _query_bootlist( self: Self, delete_logs: bool ) -> bool:
        try:
            if delete_logs and os.path.exists( self._bootlist_txtfilepath ):
                os.remove( self._bootlist_txtfilepath )
                
            process = subprocess.run(self._journal_cmd, shell=True, cwd=self._bootdir_path)
            return process.returncode == 0

        except Exception as ext:
            print(f'[BootLogManager._query_bootlist] Exception: {ext}')
            return False

    """
        _load_bootlist
            loads the text file and parses it into useful data structures
    """
    def _load_bootlist( self: Self ) -> bool:
        try:
            with open( self._bootlist_txtfilepath ) as file:
                first_line: bool = True

                for log_line in file:
                    if not first_line:
                        boot_log = BootLog( self.root_dir, log_line, self.schema_info, self.app_msgqueue, self.end_event )
                        self._bootlog_list.append( boot_log )
                        self._logdate_map[ boot_log.first_dt ] = boot_log
                        self._bootlog_index[ boot_log.boot_index ] = boot_log
                    else:
                        first_line: bool = False

            self._bootlog_list.reverse()
            return True

        except Exception as exc:
            print(f"[BootLogManager._load_txt] Exception: {exc}")

        return False

    def get_bootlog( self: Self, boot_index: int, skip_query: bool = False ) -> BootLog | None:

        if not skip_query:
            self._query_bootlist( delete_logs=False )

        if self._load_bootlist():
            boot_dir = self._bootlog_index[ boot_index ]
            boot_dir.make_dir()
            return boot_dir
        else:
            return None



