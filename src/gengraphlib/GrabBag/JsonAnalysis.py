import os
from collections import Counter

from enum import IntEnum

from datetime import datetime
import json as js
from abc import abstractmethod
from dataclasses import dataclass
from typing import NamedTuple, Self
from collections.abc import Callable

JValTypes: type = type[str, int, float, bool, datetime]

class JsonType( IntEnum ):
    str: 1
    int: 2
    float: 3
    bool: 4
    date: 4

class FieldDef( NamedTuple[str, str ] ):
    json_key: str
    log_key: str
    type: JsonType = JsonType.str
    unique: bool = True

class JsonTimestamp:
    def __init__(self: Self, dt_str: str ) -> None:
        dt_val = datetime.fromisoformat(dt_str)
        super(JsonTimestamp, self).__init__(dt_val)

key_map_list: list[FieldDef] =\
[
    ("sunit", "_SYSTEMD_UNIT"),
    ("uunit", "UNIT"),
    ("kdev", "_KERNEL_DEVICE"),
    ("usnm", "_UDEV_SYSNAME"),
    ("udnv", "_UDEV_DEVNODE"),
    ("edlk", "_UDEV_DEVLINK"),
    ("ksub", "_KERNEL_SUBSYSTEM"),
    ("tid", "TID", JsonType.int),
    ("pid", "_PID", JsonType.int),
    ("trn", "_TRANSPORT"),
    ("com", "_COMM"),
    ("pri", "PRIORITY", JsonType.int ),
    ("sid", "SYSLOG_IDENTIFIER"),
    ("time", "_SOURCE_REALTIME_TIMESTAMP", JsonType.date),
    ("fac", "SYSLOG_FACILITY"),
    ("lbk", "_LINE_BREAK", JsonType.bool),
    ("cmd", "_CMDLINE"),
    ("ounit", "OBJECT_SYSTEMD_UNIT"),
    ("cmd", "OBJECT_CMDLINE"),
    ("msg", "MESSAGE"),
    ("doc", "DOCUMENTATION")
]

json_to_log: dict[str,str] = {json:log for (json, log) in key_map_list}
log_to_json: dict[str,str] = {log:json for (json, log) in key_map_list}

@dataclass
class JsonKeyInfo:
    key: str
    total_cnt: int = 0

JObjProcessFn = Callable(dict[str,  JValTypes], bool)

@dataclass
class  JsonFieldStats[T: JValTypes]:
    log_key: str
    json_key: str
    type: JsonType
    cnt: int
    key_cnt: int
    val_cnt: int
    null_cnt: int
    unique: bool
    unique_values: Counter[T] | None

@dataclass
class JsonRecordStats(dict[str, JsonFieldStats[JValTypes]]):

    def next_record( self: Self, rec: dict[str, JValTypes ] ) -> None:
        for key, value in rec.items():
            field_stats: JsonFieldStats[JValTypes] = self[key]
            field_stats.cnt += 1
            print(f'{key}: {value}')
            match value:
                case int():
                    field_stats.val_cnt += 1
                    if field_stats.unique and field_stats.unique_values is None:
                        field_stats.unique_values = Counter[int]()
                    #field_stats.unique_values.__setitem__(value, 1)


                case float():
                    field_stats.val_cnt += 1
                    field_stats = JsonFieldStats[float]()
                case None:
                    field_stats.null_cnt += 1
                case str():
                    field_stats.val_cnt += 1
                    field_stats.unique_values[value] += 1
                case datetime():
                    field_stats.val_cnt += 1

class JObjProcess[T]:
    def __init__(self: Self) -> None:
        super(JObjProcess, self).__init__()

    @abstractmethod
    def chain(self: Self, keys: dict[str, JValTypes]) -> T:
        pass

    def dump( self: Self ) -> None:
        pass

class JsonAnalyzeKeys(JObjProcess[bool]):

    def __init__(self: Self) -> None:
        super().__init__()
        self.stats: JsonRecordStats = JsonRecordStats()

    def chain( self: Self, jdict: dict[str, JValTypes ] ) -> bool:
        self.stats.next_record( jdict )
        return True

if __name__ == "__main__":
    os.curdir = "~/data/jctl-logs"

    analysis = JsonAnalyzeKeys()

    try:
        with open("jctl-last-1.json") as file:
            for line in file:
                jobj = js.loads( line )
                analysis.chain(jobj)

        analysis.dump()

    except Exception as e:
        print(f'Exception: {e}')

    print("Done!")




