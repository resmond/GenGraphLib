import json
import subprocess

from typing import Self
import datetime as dt
import os as os

from .. import KeyValTypes
from .BootLogDir import BootLogDir

"""--------------------------------------------------------
    LogDirManagerBase __init__()
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


--------------------------------------------------------"""

class BootLogManager:

    def __init__(self: Self, root_dir: str ) -> None:
        super( BootLogManager, self ).__init__()
        self.root_dir: str = root_dir
        self.full_reparse: bool = True
        self._bootdir_path: str = os.path.join( self.root_dir, "boots" )
        self._bootlist_txtfilepath: str = os.path.join( self.root_dir, "boots", "bootlist.txt" )
        self._bootrec_jfilepath: str = os.path.join( self.root_dir, "boots", "bootlist.jline" )
        self._bootdir_list: list[BootLogDir ] = list[BootLogDir ]()
        self._bootdir_dict: dict[ dt.datetime, BootLogDir ] = {}
        self._journal_cmd = f"/bin/journalctl --list-boots > {self._bootlist_txtfilepath}"

    """
        _log_querylist
            fqueries fresh list of boot records from journalctl --list-boots as text file
    """
    def _query_bootlist( self: Self) -> bool:
        try:
            if self.full_reparse and os.path.exists( self._bootlist_txtfilepath ):
                os.remove( self._bootlist_txtfilepath )
                
            process = subprocess.run(self._journal_cmd, shell=True, cwd=self._bootdir_path)
            return process.returncode == 0

        except Exception as ext:
            print(f'[LogDirManagerBase._query_bootlist] Exception: {ext}')
            return False

    """
        _load_txt
            loads the text file and parses it into useful data structures
    """
    def _load_txt( self: Self ) -> bool:
        try:
            with open( self._bootlist_txtfilepath ) as file:
                first_line: bool = True

                for log_line in file:
                    if not first_line:
                        boot_log_dir = BootLogDir( self.root_dir, log_line )
                        self._bootdir_list.append( boot_log_dir )
                        self._bootdir_dict[ boot_log_dir.first_dt ] = boot_log_dir
                    else:
                        first_line: bool = False

            self._bootdir_list.reverse()
            return True

        except Exception as exc:
            print(f"[LogDirManagerBase._load_txt] Exception: {exc}")

        return False

    """
        _write_jfile
            serializes boot records as json lines
    """
    def _write_jfile( self: Self ) -> bool:
        try:
            with open( self._bootrec_jfilepath, "w", newline= "\n" ) as file:
                for boot_rec in self._bootdir_list:
                    file.write(boot_rec.__repr__())
                    file.write("\n")
            return True

        except Exception as exc:
            print(f"[LogDirManagerBase._write_jfile] Exception: {exc}")
            return False

    """
        exec - starts LogDirManager execution
            exec_cmd - either Full or Refresh
                Full - processes all boot records from fresh exports from journalctl
                Refresh - processes of the last two boot records from fresh exports
            specific_ndx - index of specific boot record to process else it processes them all
    """
    async def get_pipedchain( self: Self, specific_ndx: int, full_reparse: bool = True  ) -> bool:
        self.full_reparse = full_reparse

        if self.full_reparse or not self._load_txt():
            self._query_bootlist()

        if self._load_txt():
            boot_log_dir = self._bootdir_list[ specific_ndx ]
            print(f'LogDirManager.process_dirs: specific_idx: {specific_ndx}: {boot_log_dir.first_dt} ')

            cnt: int = -1
            key_values: dict[str, KeyValTypes] = {}
            line: str = ""
            try:
    
                async for line in boot_log_dir.stream():

                    try:
                        cnt += 1
                        key_values = json.loads(line)

                    except json.decoder.JSONDecodeError as jserr:
                        print(f"[LogDirManagerBase.process_bootlog] json.loads Exception: {jserr}")
                        print(f"    line:  {line}")
                        print(f"  fields:  {key_values}")

                    else:

                        try:
                            self._field_processor.process_keyvalues( key_values, cnt, line )

                        except Exception as fnexc:
                            print(f"[LogDirManagerBase.process_bootlog] self._fields_fn Exception: {fnexc}")

            except Exception as exc:
                print(f"[LogDirManagerBase.process_bootlog] boot_log_dir.streams() Exception: {exc}")
                print(f"    line:  {line}")
                print(f"  fields:  {key_values}")

        return True

