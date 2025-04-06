import os

from typing import Self

from dataclasses import dataclass
import datetime as dt
import json as js

from src.gengraphlib.GrabBag.PipedBases import PipedToFileBase

from collections.abc import AsyncGenerator
import asyncio as aio
import asyncio.subprocess as asub

from src.gengraphlib.logs.KeyGraphBase import process_fields_fn


#import asyncio as aio
#import asyncio.subprocess as asub


@dataclass
class BootRecordBase:
    idx: int
    id: str
    first_dt: dt.datetime | None = None
    last_dt: dt.datetime | None = None

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
#class BootRecCmd( StrEnum ):
#    Init    = "Init"
#    ExportKeys  = "ExportKeys"



class BootLogDirBase:

    def __init__(self: Self, root_dir: str, log_line: str ) -> None:
        super().__init__()
        self.root_dir = root_dir

        try:
            val_list: list[str] = log_line.split()
            self.idx: int = int(val_list[0])
            self.id: str = val_list[1]

            _first_dt: str = " ".join(val_list[3:5])
            _last_dt: str = " ".join(val_list[7:9])

            self.first_dt: dt.datetime = dt.datetime.fromisoformat(_first_dt)
            self.last_dt: dt.datetime = dt.datetime.fromisoformat(_last_dt)
            self.dir_name = self.first_dt.isoformat()
            self.dir_path = os.path.join(self.root_dir, self.dir_name)

            self.exec_process: asub.Process | None = None
            self.cmd: str | None = None
            self.started: bool = False
            self.error: int = 0
            self.exc: Exception | None = None

        except Exception as _ect:
            print(f'[BootLogDirBase.__init__] Exception: {_ect}')
            self.error = -1
            self.exc = _ect
            return

    @classmethod
    def from_dict(cls, d: dict) -> Self:
        return BootRecordBase(idx=d["idx"], id=d["id"], first_dt=d["first_dt"], last_dt=d["last_dt"])

    def __repr__(self: Self ) -> str:
        return f'{{"idx":{self.idx}, "id":"{self.id}", "first_dt":"{self.first_dt}", "last_dt":"{self.last_dt}"}}'

    def __str__(self) -> str: return self.__repr__()

    def __repr__(self: Self) -> str:
        return f'{{"dir_name":"{self.dir_name}", "dir_path":"{self.dir_path}", "keys_filepath":"{self.keys_filepath}"}}'

    def __str__(self: Self) -> str: return self.__repr__()

    def _dir_exists( self: Self ) -> bool:
        try:
            #dir_name = self.first_dt.isoformat()
            #dir_path = os.path.join(self.root_dir, dir_name)
            os.makedirs( self.dir_path, exist_ok=True )
            return True

        except Exception as e:
            print(f'[BootLogDirBase._dir_exists] Exception: {e}')
            return False

    async def stream( self: Self ) -> AsyncGenerator[ str, None ]:
        try:
            cmd: str = f"journalctl -b {self.id} -o json"
            if self._dir_exists():
                self.exec_process: asub.Process = await aio.create_subprocess_shell(
                    cmd,
                    cwd=self.dir_path,
                    stdout=aio.subprocess.PIPE,
                )

                while True:
                    try:
                        line = await self.exec_process.stdout.readline()
                    except aio.exceptions.TimeoutError as aioerr:
                        print(f'[BootLogDirBase.stream] Exception: {aioerr}')
                        break;
                    else:
                        if line:
                            try:
                                yield line.decode().strip()
                            except Exception as decode_err:
                                print(f'[BootLogDirBase.stream] Exception: {decode_err}')
                        else:
                            break

        except Exception as e:
            print(f"[BootLogDirBase.stream] Exception: {e}")

    async def run_command(
        self: Self, cmd: str, exec_dir: str
    ) -> AsyncGenerator[str, None]:
        try:
            self.exec_process: asub.Process = await aio.create_subprocess_shell(
                cmd,
                cwd=exec_dir,
                stdout=aio.subprocess.PIPE,
            )

            while True:
                line = await self.exec_process.stdout.readline()
                if line:
                    yield line.decode().strip()
                else:
                    break

        except Exception as exc:
            print(f"[BootLogDirBase.run_command]: {exc}")
            self.exc = exc
            self.error = -1
