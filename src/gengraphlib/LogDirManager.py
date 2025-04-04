import subprocess
from abc import abstractmethod

from enum import StrEnum

from typing import Self

from logs.BootLogDir import BootRecordBase
from logs.BootLogDir import BootLogDirBase

import datetime as dt
#import asyncio as aio
import io as io
import os as os

class ManagerCmd( StrEnum ):
    Full    = "Full"
    Refresh = "Refresh"

"""
    LogDirManager
"""
class LogDirManagerBase:
    """
    LogDirManager __init__()
        root_dir - root of all log data
            root_dir/boots/{fulldate}/ files - being primary log data for a single boot history
            root_dir/keys - being primary key analysis data for ALL boots

        self.root_dir = rot_dir
        self._cmd - last command executed
        self._bootlist_txtfilepath - path to "bootlist.txt" from 'journalctl --list-boots'
        self._bootrec_jfilepath: str = path to "bootlist.jline" json line data of --list-boots
        self._bootrec_list: list[BootRecord ] = tuple data for basic boot history entries
        self._bootdir_dict: dict[ dt.datetime, BootLogDir ] = dict of BootLogDir boot manager objects
        self._journal_cmd = "journalctl -b 0 -o json" = basic journalctl command for a single boot export to json

    """
    def __init__(self: Self, root_dir: str) -> None:
        super().__init__()
        self.root_dir: str = root_dir
        self._cmd: ManagerCmd | None = None
        self._bootlist_txtfilepath: str = os.path.join( self.root_dir, "bootlist.txt" )
        self._bootrec_jfilepath: str = os.path.join( self.root_dir, "bootlist.jline" )
        self._bootrec_list: list[BootRecordBase] = list[BootRecordBase]()
        self._bootdir_dict: dict[ dt.datetime, BootLogDirBase ] = {}
        self._journal_cmd = "journalctl -b 0 -o json"


    """
        exec - starts LogDirManager execution
            exec_cmd - either Full or Refresh
                Full - processes all boot records from fresh exports from journalctl
                Refresh - processes of the last two boot records from fresh exports
            specific_ndx - index of specific boot record to process else it processes them all
    """
    async def exec( self, exec_cmd: ManagerCmd, specific_ndx: int | None ) -> bool:
        self._cmd = exec_cmd

        if self._cmd == ManagerCmd.Full or not self._load_txt():
            self._log_querylist( exec_cmd == ManagerCmd.Full )

        if self._load_txt():
            return self.process_dirs( specific_ndx )
        else:
            return False

    """
        _log_querylist
            fqueries fresh list of boot records from journalctl --list-boots as text file
    """
    def _log_querylist( self: Self, del_existing: bool ) -> bool:
        try:
            if del_existing and os.path.exists( self.bootlist_txtfilepath ):
                os.remove( self.bootlist_txtfilepath )
                
            journalctl_cmd: str = "/bin/journalctl --list-boots > bootlist.txt"
            process = subprocess.run(journalctl_cmd, shell=True, cwd=self.root_dir)
            return process.returncode == 0

        except Exception as ext:
            print(f'[export_log] Exception: {ext}')
            return False

    """
        _load_txt
            loads the text file and parses it into useful data structures
    """
    def _load_txt( self ) -> bool:
        try:
            with open( self._bootlist_txtfilepath ) as file:
                first_line: bool = True

                for line in file:
                    if not first_line:
                        boot_rec = BootRecordBase.parse_line(line)
                        self._bootrec_list.append( boot_rec )
                        boot_rec.bootlog_dir = BootLogDirBase( self.root_dir, boot_rec )
                        self._bootdir_dict[ boot_rec.first_dt ] = boot_rec.bootlog_dir
                    else:
                        first_line: bool = False

            self._bootrec_list.reverse()
            return True

        except Exception as exc:
            print(f"[LogDirManager._load_txt] Exception: {exc}")

        return False

    """
        _write_jfile
            serializes boot records as json lines
    """
    def _write_jfile( self: Self ) -> bool:
        try:
            with open( self._bootrec_jfilepath, "w", newline= "\n" ) as file:
                for boot_rec in self._bootrec_list:
                    file.write(boot_rec.__repr__())
                    file.write("\n")
            return True

        except Exception as exc:
            print(f"[LogDirManager._write_jfile] Exception: {exc}")
            return False

    """
        _load_jfile
            loads the json lines file skipping requerying journalctl
    """
    def _load_jfile( self: Self ) -> bool:
        try:
            with io.open( self._bootrec_jfilepath ) as file:
                for line in file:
                    boot_rec = BootRecordBase.parse_json( line )
                    if boot_rec is not None:
                        self._bootrec_list.append( boot_rec )
                        boot_rec.bootlog_dir = BootLogDirBase( self.root_dir, boot_rec )
                        self._bootdir_dict[ boot_rec.first_dt ] = boot_rec.bootlog_dir
            return True

        except Exception as ext:
            print(f'[LogDirManager._load_jfile] Exception: {ext}')
            return False

    """
        process_dirs
            either selects a specific boot record to loops through them all and calls BootRecDir.exec() on each
    """
    def process_dirs( self: Self, specific_idx: int | None = None ) -> bool:
        if specific_idx is not None:
            boot_rec = self.boot_recs[ specific_idx ]
            print(f'LogDirManager.process_dirs: specific_idx: {specific_idx}: {boot_rec.first_dt} ')
            return self.process_dir( boot_rec)
        else:
            for boot_rec in self._bootrec_list:
                if not self.process_dir( boot_rec ):
                    print(f'LogDirManager.process_dirs: failed: {boot_rec.id}:{boot_rec.first_dt}')
                    return False
        return True

    """
        process_dir
    """
    @abstractmethod
    def process_dir( self: Self, boot_rec: BootRecordBase ) -> bool:
        pass

"""
if __name__ == "__main__":
    print("[LodDirManager] starting main")

    try:
        data_root: str = "/home/richard/data/jctl-logs"
        logdir_manager = LogDirManager(data_root)
        aio.run( logdir_manager.exec( ManagerCmd.Full, 0 ) )

    except Exception as e:
        print(f"[LodDirManager] Exception: {e}")

    print("[LodDirManager] done")
"""


