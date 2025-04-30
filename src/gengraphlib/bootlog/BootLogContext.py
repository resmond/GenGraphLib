from typing import Self

import datetime as dt
import os

from io import BufferedWriter, TextIOWrapper, BufferedReader

from ..common import BootLogInfo


class BootLogContext:
    def __init__(self: Self, boot_log_info: BootLogInfo) -> None:
        super().__init__()
        self._info: BootLogInfo = boot_log_info
        self.boot_id: str = self._info.boot_id

    @property
    def boot_dir(self: Self) -> str:
        return self._info.dir_path

    @property
    def keys_filepath(self: Self) -> str:
        return self._info.keys_path

    @property
    def boot_index(self: Self) -> int:
        return self._info.boot_index

    @property
    def schema_bootid( self: Self ) -> str:
        return self.boot_id

    @property
    def first_dt(self: Self) -> dt.datetime:
        return self._info.first_dt

    @property
    def last_dt(self: Self) -> dt.datetime:
        return self._info.last_dt

    def create_writable_file(self: Self, file_name: str, binary: bool = False ) -> BufferedWriter | TextIOWrapper | None:
        try:
            filepath: str = os.path.join( self._boot_dir, file_name )
            if binary:
                return open(filepath, 'wb')
            else:
                return open(filepath, 'w')

        except Exception as e:
            print(f'[BootLogIoContext.create_writable_file] Exception: {e}')
            return None

    def create_readable_file(self: Self, file_name: str, binary: bool ) -> BufferedReader | TextIOWrapper | None:
        try:
            filepath: str = os.path.join( self._boot_dir, file_name )
            if binary:
                return open(filepath, 'rb')
            else:
                return open(filepath)

        except Exception as e:
            print(f'[BootLogIoContext.create_readable_file] Exception: {e}')
            return None
