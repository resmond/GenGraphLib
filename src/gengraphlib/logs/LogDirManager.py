from asyncio import subprocess

from enum import StrEnum

from typing import Self

from BootLogDir import BootRecord, BootLogDir

import datetime as dt
import asyncio as aio
import io as io
import os as os
import json as js

class CommandEnum(StrEnum):
    Full    = "Full"
    Refresh = "Refresh"

class LogDirManager:

    def __init__(self: Self, root_dir: str) -> None:
        super().__init__()
        self.root_dir: str = root_dir
        self.cmd: CommandEnum | None = None
        self.bootlist_txtfilepath: str = os.path.join( self.root_dir, "bootlist.txt" )
        self.bootrec_jfilepath: str = os.path.join( self.root_dir, "bootlist.jline" )
        self._load_boots: list[BootRecord] = list[BootRecord]()
        self.bootdir_dict: dict[ dt.datetime, BootLogDir ] = {}
        self.journal_cmd = "journalctl -b 0 -o json"

    async def exec( self, exec_cmd: CommandEnum ) -> bool:
        self.cmd = exec_cmd

        if self.cmd == CommandEnum.Full or not self._load_txt():
            self._log_querylist()

        if self._load_txt():
            return self.process_dirs()
        else:
            return False

    def _log_querylist( self: Self ) -> bool:
        try:
            os.remove( self.bootlist_txtfilepath )
            journalctl_cmd: str = f"journalctl --list-boots > {self.bootlist_txtfilepath}"
            process = subprocess.run(args=journalctl_cmd, shell=True, cwd=self.root_dir)
            return process.returncode == 0

        except Exception as e:
            print(f'[export_log] Exception: {e}')
            return False

    def _load_txt( self ) -> bool:
        try:
            with open( self.bootlist_txtfilepath ) as file:
                first_line: bool = True

                for line in file:
                    if not first_line:
                        boot_rec = BootRecord.parse_line(line)
                        self._load_boots.append(boot_rec)
                    else:
                        first_line: bool = False

            self._load_boots.reverse()
            return True

        except Exception as exc:
            print(f"[LogDirManager._load_txt] Exception: {exc}")

        return False

    def _write_jfile( self: Self ) -> bool:
        try:
            with open(self.bootrec_jfilepath, "w", newline="\n") as file:
                for boot_rec in self._load_boots:
                    file.write(boot_rec.__repr__())
                    file.write("\n")
            return True

        except Exception as exc:
            print(f"[LogDirManager._write_jfile] Exception: {exc}")
            return False

    def _load_jfile( self: Self ) -> bool:
        try:
            with io.open( self.bootrec_jfilepath ) as file:
                for line in file:
                    self._bootref_jline( line )

            return True

        except Exception as ext:
            print(f'[LogDirManager._load_jfile] Exception: {ext}')
            return False

    def _bootref_jline( self: Self, ref_line: str ) -> bool:

        boot_rec = BootRecord.parse_json( ref_line )
        if boot_rec is not None:
            self._load_boots.append(boot_rec)
            self.bootdir_dict[ boot_rec.first_dt ] = boot_rec
            return True

        return False

    def process_dirs( self: Self, from_json: bool = False, specific_idx: int | None = None ) -> bool:
        loaded: bool = False
        if not from_json:
            loaded = self._load_txt()
        else:
            loaded = self._load_jfile()

        if loaded:
            if specific_idx:
                return self.process_dir( self.boot_recs[ specific_idx ])
            else:

                for boot_rec in self._load_boots:
                    loaded = self.process_dir( boot_rec )

        return loaded

    def process_dir( self: Self, boot_rec: BootRecord ) -> bool:
        boot_log_dir = BootLogDir( self.root_dir, boot_rec )
        self.bootdir_dict[ boot_rec.first_dt ] = boot_log_dir
        boot_log_dir.log_fromquery()
        return True

if __name__ == "__main__":
    print("[LodDirManager] starting main")

    try:
        data_root: str = "~/data/jctl-logs/"
        logdir_manager = LogDirManager(data_root)
        aio.run(logdir_manager.exec(CommandEnum.Full))

    except Exception as e:
        print(f"[LodDirManager] Exception: {e}")

    print("[LodDirManager] done")



