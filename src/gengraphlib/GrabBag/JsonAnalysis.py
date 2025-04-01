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
    JString = 1
    JInt    = 2
    JFloat  = 3
    JBool   = 4
    JDate   = 5

class FieldDef(NamedTuple):
    json_key: str
    log_key: str
    type: JsonType = JsonType.JString
    unique: bool = True

class JsonTimestamp:
    def __init__(self: Self, dt_str: str ) -> None:
        dt_val = datetime.fromisoformat(dt_str)
        super(JsonTimestamp, self).__init__(dt_val)

key_map_list: list[FieldDef] = [
    ("sunit", "_SYSTEMD_UNIT"),                                # 1
    ("uunit", "UNIT"),                                         # 1
    ("usnm", "_UDEV_SYSNAME"),                                 # 1
    ("udnv", "_UDEV_DEVNODE"),                                 # 1
    ("ksub", "_KERNEL_SUBSYSTEM"),                             # 1
    ("tid", "TID", JsonType.JInt),                              # 1
    ("com", "_COMM"),
    ("sid", "SYSLOG_IDENTIFIER"),                              # 1
    ("time", "_SOURCE_REALTIME_TIMESTAMP", JsonType.JDate),
    ("fac", "SYSLOG_FACILITY"),
    ("lbk", "_LINE_BREAK", JsonType.JBool),
    ("cmd", "_CMDLINE"),
    ("uiid", "USER_INVOCATION_ID"),                            # 1
    ("gapi", "GLIB_OLD_LOG_API"),
    ("nmd", "NM_DEVICE"),
    ("gld", "GLIB_DOMAIN"),
    ("nmlev", "NM_LOG_LEVEL"),
    ("jres", "JOB_RESULT"),
    ("stmst", "_SOURCE_MONOTONIC_TIMESTAMP"),
    ("jid", "JOB_ID"),
    ("jtp", "JOB_TYPE"),
    ("iid", "INVOCATION_ID"),
    ("stmst", "SYSLOG_TIMESTAMP"),
    ("mid", "MESSAGE_ID"),
    ("pid", "SYSLOG_PID"),
    ("sunit", "_SYSTEMD_USER_UNIT"),                           # 1
    ("souid", "_SYSTEMD_OWNER_UID"),                           # 1
    ("stid", "_STREAM_ID"),                                    # 1
    ("auses", "_AUDIT_SESSION"),
    ("cdfn", "CODE_FUNC"),
    ("cdln", "CODE_LINE"),
    ("cdfl", "CODE_FILE"),
    ("siid", "_SYSTEMD_INVOCATION_ID"),                        # 1
    ("exe", "_EXE"),
    ("sdslc", "_SYSTEMD_SLICE"),
    ("linctx", "_SELINUX_CONTEXT"),
    ("uid", "_UID"),
    ("cur", "__CURSOR")


#    ("cmd", "OBJECT_CMDLINE"),  #
#    ("kdev", "_KERNEL_DEVICE"),  #
#    ("edlk", "_UDEV_DEVLINK"),  #
#    ("pid", "_PID", JsonType.int),  #
#    ("trn", "_TRANSPORT"),  #
#    ("pri", "PRIORITY", JsonType.int),  #
#    ("ounit", "OBJECT_SYSTEMD_UNIT"),  #
#    ("msg", "MESSAGE"),  #
#    ("doc", "DOCUMENTATION"),  #
]

capture_list: list[str] = [
    "sunit",
    "uunit",
    "usnm",
    "udnv",
    "ksub",
    "tid",
    "sid",
    "uiid",
    "sunit",
    "souid",
    "stid",
    "siid",
    "sdslc",
    "linctx",
    "uid"
]

json_to_log: dict[str,str] = {json:log for (json, log) in key_map_list}
log_to_json: dict[str,str] = {log:json for (json, log) in key_map_list}

print_dict: dict[str, list[str]] = dict[str,list[str]]()
capture_flags: dict[str, bool ] = {}

for (json, log) in key_map_list:
    print_dict[json] = []
    capture_flags[log] = False

for key in capture_list:
    capture_flags[key] = False

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
        for rec_key, rec_value in rec.items():
            field_stats: JsonFieldStats[JValTypes] = self[rec_key]
            field_stats.cnt += 1
            print(f'{rec_key}: {rec_value}')
            match rec_value:
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
                    field_stats.unique_values[rec_value] += 1
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




