import datetime as dt

from dataclasses import dataclass

@dataclass
class BootLogInfo:
    schema_bootid: str
    boot_index: int
    first_dt: dt.datetime
    last_dt: dt.datetime
    dir_name: str
    dir_path: str
    keys_path: str = None

