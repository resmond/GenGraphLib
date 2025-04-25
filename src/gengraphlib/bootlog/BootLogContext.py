from typing import Self

import datetime as dt
import os

from io import BufferedWriter, TextIOWrapper, BufferedReader

from ..common import BootLogInfo


class BootLogContext:
    def __init__(self: Self, boot_log_info: BootLogInfo) -> None:
        self.boot_log_info: BootLogInfo = boot_log_info
        self._schema_bootid: str = boot_log_info.schema_bootid
        self._boot_dir: str = boot_log_info.dir_path
        self._keys_filepath: str = boot_log_info.keys_path

    @property
    def boot_dir(self: Self) -> str:
        return self._boot_dir

    @property
    def keys_filepath(self: Self) -> str:
        return self._keys_filepath

    @property
    def boot_index(self: Self) -> int:
        return self._boot_index

    @property
    def schema_bootid( self: Self ) -> str:
        return self._schema_bootid

    @property
    def first_dt(self: Self) -> dt.datetime:
        return self.boot_log_info.first_dt

    @property
    def last_dt(self: Self) -> dt.datetime:
        return self.boot_log_info.last_dt

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
