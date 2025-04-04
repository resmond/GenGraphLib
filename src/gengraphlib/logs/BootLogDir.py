from abc import abstractmethod
from enum import StrEnum

import os

from typing import Self

from dataclasses import dataclass
import datetime as dt
import subprocess
import json as js

from src.gengraphlib.fileparse.PipedBases import PipedToFileBase

#import asyncio as aio
#import asyncio.subprocess as asub


@dataclass
class BootRecordBase:
    idx: int
    id: str
    first_dt: dt.datetime | None = None
    last_dt: dt.datetime | None = None
    #bootlog_dir: BootLogDir | None = None

    @classmethod
    def from_dict(cls, d: dict) -> Self:
        return BootRecordBase(idx=d["idx"], id=d["id"], first_dt=d["first_dt"], last_dt=d["last_dt"])

    def __repr__(self: Self ) -> str:
        return f'{{"idx":{self.idx}, "id":"{self.id}", "first_dt":"{self.first_dt}", "last_dt":"{self.last_dt}"}}'
    def __str__(self) -> str: return self.__repr__()

    @classmethod
    def parse_line( cls, line: str ) -> Self:
        val_list: list[str] = line.split()
        idx: str = val_list[0]
        id: str = val_list[1]
        first: str = " ".join(val_list[3:5])
        last: str = " ".join(val_list[7:9])
        boot_rec = BootRecordBase(
            int(idx),
            id,
            dt.datetime.fromisoformat(first),
            dt.datetime.fromisoformat(last),
        )
        return boot_rec

    @classmethod
    def parse_json( cls, json_str: str ) -> Self | None:
        try:
            ref_dict = js.loads(json_str.strip())
            first_dt: dt.datetime = dt.datetime.fromisoformat(ref_dict["first_dt"])
            last_dt: dt.datetime = dt.datetime.fromisoformat(ref_dict["last_dt"])
            boot_rec = BootRecordBase(
                idx=int(ref_dict["idx"]),
                id=ref_dict["id"],
                first_dt=first_dt,
                last_dt=last_dt,
            )
            return boot_rec

        except js.JSONDecodeError as jsext:
            print(f'[BootRecord.parse_json] JSONDecodeError: {jsext}')
            print(f'   [{jsext.colno}={json_str[jsext.colno]}]: {json_str}')
            return None

        except Exception as ext:
            print(f'[BootRecord.parse_json] Exception: {ext}')
            return None

class PipedToKeys(PipedToFileBase):
    def __init__( self: Self, output_filepath: str ) -> None:
        super().__init__("PipedToKeys", output_filepath )

    def process_line( self: Self, line: str ) -> bool:
        return True
"""
    BootRecCmd
        Init - 
            test or creat /boot/{boot-first-datatime} directory
            export boot-log using journalctl to stdout
            readlines async and parse / remap data into json key-value fields
            write data into jline file
            
        ExportKeys - 
            slice and split key-value data into keys/key directories
            
"""
class BootRecCmd( StrEnum ):
    Init    = "Init"
    ExportKeys  = "ExportKeys"



class BootLogDirBase:

    def __init__(self: Self, root_dir: str, boot_rec: BootRecordBase) -> None:
        super().__init__()
        self.boot_rec = boot_rec
        self.root_dir = root_dir
        self.dir_name = self.boot_rec.first_dt.isoformat()
        self.dir_path = os.path.join(self.root_dir, self.dir_name)

    @property
    def idx(self: Self) -> int:
        return self.boot_rec.idx

    @property
    def id(self: Self) -> str:
        return self.boot_rec.id

    @property
    def first_dt(self: Self) -> dt.datetime:
        return self.boot_rec.first_dt

    @property
    def last_dt(self: Self) -> dt.datetime:
        return self.boot_rec.last_dt

    def __repr__(self: Self) -> str:
        return f'{{"dir_name":"{self.dir_name}", "dir_path":"{self.dir_path}", "keys_filepath":"{self.keys_filepath}"}}'

    def __str__(self: Self) -> str: return self.__repr__()

    @abstractmethod
    def exec_cmd( self: Self, cmd: BootRecCmd ) -> bool:
        return True

    def _dir_exists( self: Self ) -> bool:
        try:
            dir_name = self.boot_rec.first_dt.isoformat()
            dir_path = os.path.join(self.root_dir, dir_name)
            os.makedirs( dir_path, exist_ok=True )
            return True

        except Exception as e:
            print(f'[make_dir] Exception: {e}')
            return False

    def log_fromquery( self: Self ) -> bool:
        try:
            boot_id = self.boot_rec.id
            if self._dir_exists():
                # list[str] = [f"journalctl -b {boot_id} -o json","| python3 KeyMaps.py", f"> {self.keys_filepath}"]
                journalctl_cmd: str = f"journalctl -b {boot_id} -o json > {self.keys_filepath}"
                result = subprocess.run(args=journalctl_cmd, shell=True, cwd=self.dir_path)
                print(f'stderr: {result.stderr}')

            return True

        except Exception as e:
            print(f'[export_log] Exception: {e}')
            return False




