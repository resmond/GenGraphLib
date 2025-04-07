import os

from typing import Self

import datetime as dt
import asyncio.subprocess as asub

from collections.abc import AsyncGenerator

from ..fileparse.CmdStreamBase import  CmdStreamBase

class BootLogDirBase:

    def __init__( self: Self, root_dir: str, log_rec: str ) -> None:
        super().__init__()
        self.root_dir = root_dir

        self.idx: int = 0
        self.id: str = ""
        self.dir_name: str = ""
        self.dir_path: str = ""
        self.first_dt: dt.datetime
        self.last_dt: dt.datetime

        self.exec_process: asub.Process | None = None
        self.cmd: str = f"journalctl -b {self.id} -o json"
        self.started: bool = False
        self.error: int = 0
        self.exc: Exception | None = None
        self.CmdStream: CmdStreamBase | None = None

        try:
            val_list: list[str] = log_rec.split()
            self.idx = int(val_list[0])
            self.id = val_list[1]

            _first_dt: str = " ".join(val_list[3:5])
            _last_dt: str = " ".join(val_list[7:9])

            self.first_dt = dt.datetime.fromisoformat(_first_dt)
            self.last_dt = dt.datetime.fromisoformat(_last_dt)
            self.dir_name = self.first_dt.isoformat()
            self.dir_path = os.path.join(self.root_dir, "boots", self.dir_name)

            self.CmdStream = CmdStreamBase(cmd=self.cmd, exec_dir=self.dir_path)

        except Exception as _ect:
            print(f"[BootLogDirBase.__init__] Exception: {_ect}")
            self.error = -1
            self.exc = _ect
            return

    def __repr__(self: Self) -> str:
        return f'{{idx:{self.idx}, id:{self.id}, first_dt:{self.first_dt}, last_dt:{self.last_dt}, dir_name:{self.dir_name}, dir_path:{self.dir_path}, keys_filepath:{self.keys_filepath}}}'

    def __str__(self: Self) -> str: return self.__repr__()

    def _dir_exists( self: Self ) -> bool:
        try:
            os.makedirs( self.dir_path, exist_ok=True )
            return True

        except Exception as e:
            print(f'[BootLogDirBase._dir_exists] Exception: {e}')
            return False

    async def stream( self: Self ) -> AsyncGenerator[ str, None ]:
        if self._dir_exists():
            async for line in self.CmdStream.run_command(self.cmd, self.dir_path):
                yield line

