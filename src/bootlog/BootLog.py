from typing import Self
import os
import datetime as dt

from loguru import logger

class BootLog:

    def __init__( self: Self, root_dir: str, logrec_line: str ) -> None:
        super().__init__()

        self.root_dir = root_dir

        val_list: list[str] = logrec_line.split()
        boot_index = int( val_list[0] )
        boot_id    = val_list[1]
        first_dt   = dt.datetime.fromisoformat(" ".join(val_list[3:5]))
        last_dt    = dt.datetime.fromisoformat(" ".join(val_list[7:9]))
        yymmdd     = first_dt.strftime("%y-%m-%d")
        hhmm       = first_dt.strftime("%H-%M")

        self.bool_label: str = f"{yymmdd}:{hhmm}"

        bootlog_path = os.path.join( self.root_dir, "boots", self.bool_label )

        self.boot_index:   int         = boot_index
        self.boot_id:      str         = boot_id

        self.first_dt:     dt.datetime = first_dt
        self.last_dt:      dt.datetime = last_dt
        self.bootlog_path: str         = bootlog_path

    def make_dir( self: Self ) -> bool:
        try:
            os.makedirs( self.bootlog_path, exist_ok=True )
            return True

        except Exception as e:
            logger.error(f'Exception: {e}')
            return False

    def __repr__( self: Self ) -> str:
        return f'{{idx:{self.boot_index}, id:{self.boot_id}, first_dt:{self.first_dt}, last_dt:{self.last_dt}, dir_name:{self.boot_label()}, dir_path:{self.bootlog_path}, keys_filepath:{self.keys_path}}}'

    def __str__( self: Self ) -> str: return self.__repr__()





