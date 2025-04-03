import json
import os.path
from typing import Self
from enum import IntEnum
from datetime import datetime
from sortedcontainers import SortedDict
from abc import ABC, abstractmethod

from progress.bar import Bar

KValTypes: type = type[str, int, bool, datetime ]

class KeyType( IntEnum ):
    KStr         = 1
    KInt         = 2
    KBool        = 3
    KTimeStamp   = 4

class JsonTimestamp:
    def __init__(self: Self, dt_str: str ) -> None:
        dt_val = datetime.fromisoformat(dt_str)
        super(JsonTimestamp, self).__init__(dt_val)

class LineNumList(list[int]):
    pass

class AbcKeyValues[T: KValTypes](ABC, SortedDict[T,LineNumList]):
    def __init__(self: Self) -> None:
        super().__init__()
        self.unique: bool = True
        self._cnt: int = 0

    def add_value(self: Self, new_value: T, line_num: int) -> None:
        if new_value not in self:
            self[new_value] = []
        else:
            self.unique = False
            
        self[new_value].append( line_num )
        self._cnt += 1

class AbcKeyDef[T: KValTypes](ABC, AbcKeyValues[T]):
    def __init__( self: Self, _json_key: str, _log_key: str) -> None:
        self.json_key: str = _json_key
        self.log_key: str = _log_key
        self.key_type: KeyType = KeyType.KStr
        self.key_values: AbcKeyValues[T] = AbcKeyValues[T]()
        
    def add_value( self: Self, new_value: T, line_num: int ) -> None:
        self.key_values.add_value(new_value, line_num)

    @abstractmethod
    def add_str_value( self: Self, str_value: str, line_num: int ) -> None:
        pass
        
class StrKeyDef( AbcKeyDef[str ] ):
    def __init__( self, _json_key: str, _log_key: str ):
        self.key_type = KeyType.KStr
        super( StrKeyDef, self ).__init__( _log_key, _json_key )

    def add_str_value( self: Self, str_value: str, line_num: int ) -> None:
        self.key_values.add_value( str_value, line_num )

class IntKeyDef( AbcKeyDef[int ] ):
    def __init__( self, _json_key: str, _log_key: str ):
        self.key_type = KeyType.KInt
        super( IntKeyDef, self ).__init__( _log_key, _json_key )

    def add_str_value( self: Self, str_value: str, line_num: int ) -> None:
        self.key_values.add_value( int(str_value), line_num )

class BoolKeyDef( AbcKeyDef[bool ] ):
    def __init__( self, _json_key: str, _log_key: str ):
        self.key_type = KeyType.KBool
        super( BoolKeyDef, self ).__init__( _log_key, _json_key )

    def add_str_value( self: Self, str_value: str, line_num: int ) -> None:
        self.key_values.add_value( bool(str_value), line_num )

class TmstKeyDef( AbcKeyDef[datetime ] ):
    def __init__( self, _json_key: str, _log_key: str ):
        self.key_type = KeyType.KTimeStamp
        super( TmstKeyDef, self ).__init__( _log_key, _json_key )

    def add_str_value( self: Self, str_value: str, line_num: int ) -> None:
        try:
            datetime_value = datetime.fromisoformat(str_value)
            self.key_values.add_value( datetime_value, line_num )
        except ValueError as e:
            print(f'[TmstKeyDef.add_str_value] ValueError: {e} - "{str_value}"')

class KeySet[T: KValTypes](list[AbcKeyDef[T]]):
    pass

class KeyGroups( dict[str, KeySet ] ):
    def __init__( self: Self, graph_root: dict[str,AbcKeyDef ] ) -> None:
        self.graph_root: dict[str,AbcKeyDef ] = graph_root
        super().__init__()

    def add_keygroup( self: Self, keygroup_name: str ) -> None:
        self[ keygroup_name] = list[AbcKeyDef ]

    def add_key_to_group( self: Self, _keygroup_name: str, _key_def: AbcKeyDef ) -> None:
        self[_keygroup_name].__setitem__( _key_def.json_key, _key_def )

    def add_keys_to_group( self: Self, _keygroup_name: str, keys: iter( str ) ) -> None:
        for _json_key in keys:
            _key_def = self.graph_root[_json_key]
            self.add_key_to_group( _keygroup_name, _key_def )

class KeyGraphRoot( dict[str, AbcKeyDef ] ):
    def __init__(self: Self, root_dir: str) -> None:
        super().__init__()
        self._root_dir = root_dir
        self._log_keys: dict[str,AbcKeyDef ] = dict[str,AbcKeyDef ]()
        self.key_groups: KeyGroups = KeyGroups(self)
        self.missing_keys: list[str] = []

    def by_logkey( self: Self, _log_key_str: str ) -> AbcKeyDef:
        return self._log_keys[_log_key_str]

    def add_keydef( self: Self, _key_def: AbcKeyDef ) -> None:
        self[_key_def.json_key] = _key_def
        self._log_keys[_key_def.log_key] = _key_def

    def add_keydefs( self: Self, _keydefs: list[AbcKeyDef ] ) -> None:
        for _key_def in _keydefs:
            self.add_keydef(_key_def)

    def new_keygroup_with_keys( self: Self, _keygroup_name: str, _keys: iter(str) ) -> None:
        self.key_groups.add_keygroup( _keygroup_name )
        self.key_groups.add_key_to_group( _keygroup_name, _keys )
        
    def process_fields( self, fields: dict[str,str], line_num: int ) -> bool:
        result = True
        for log_key, value in fields.items():
            if log_key in self._log_keys:
                json_key = self._log_keys[log_key].json_key
                self[json_key].add_str_value( value, line_num )
            else:
                self.missing_keys.append( log_key )
                result = False
        return result

class JsonLogKeyGraph( KeyGraphRoot ):
    def __init__( self: Self, log_root: str ) -> None:
        super( JsonLogKeyGraph, self ).__init__( log_root )
        self.add_keydefs([
            StrKeyDef( "sysUnit", "_SYSTEMD_UNIT" ),                                  # id?
            StrKeyDef( "usrUnit", "UNIT" ),                                           # id?
            StrKeyDef( "udSName", "_UDEV_SYSNAME" ),                                  # id?
            StrKeyDef( "udDvNd", "_UDEV_DEVNODE" ),                                   # id?
            StrKeyDef( "krSubSys", "_KERNEL_SUBSYSTEM" ),                             # id?
            IntKeyDef( "tID", "TID" ),                                                # id?
            StrKeyDef( "comm", "_COMM" ),
            StrKeyDef( "slID", "SYSLOG_IDENTIFIER" ),                                 # id?
            TmstKeyDef( "srTime", "_SOURCE_REALTIME_TIMESTAMP" ),
            StrKeyDef( "sysFac", "SYSLOG_FACILITY" ),
            BoolKeyDef( "lnBk", "_LINE_BREAK" ),
            StrKeyDef( "cmdLn", "_CMDLINE" ),
            StrKeyDef( "usrInvID", "USER_INVOCATION_ID" ),                            # id?
            StrKeyDef( "glbLogApi", "GLIB_OLD_LOG_API" ),
            StrKeyDef( "nmDev", "NM_DEVICE" ),                                        # id?
            StrKeyDef( "glbDom", "GLIB_DOMAIN" ),                                     # id?
            StrKeyDef( "nmLogLev", "NM_LOG_LEVEL" ),
            StrKeyDef( "jbRes", "JOB_RESULT" ),
            StrKeyDef( "smTime", "_SOURCE_MONOTONIC_TIMESTAMP" ),
            StrKeyDef( "jbID", "JOB_ID" ),                                            # id?
            StrKeyDef( "jbType", "JOB_TYPE" ),
            StrKeyDef( "invID", "INVOCATION_ID" ),                                    # id?
            StrKeyDef( "slTime", "SYSLOG_TIMESTAMP" ),
            StrKeyDef( "msgID", "MESSAGE_ID" ),                                       # id?
            StrKeyDef( "slPID", "SYSLOG_PID" ),                                       # id?
            StrKeyDef( "sysdUsrUnit", "_SYSTEMD_USER_UNIT" ),                         # id?
            StrKeyDef( "ssysdUwnUID", "_SYSTEMD_OWNER_UID" ),                         # id?
            StrKeyDef( "strmID", "_STREAM_ID" ),                                      # id?
            StrKeyDef( "audSes", "_AUDIT_SESSION" ),
            StrKeyDef( "cdFn", "CODE_FUNC" ),
            StrKeyDef( "cdLn", "CODE_LINE" ),
            StrKeyDef( "cdFl", "CODE_FILE" ),
            StrKeyDef( "sysdInvID", "_SYSTEMD_INVOCATION_ID" ),                       # id?
            StrKeyDef( "exe", "_EXE" ),                                               # id?
            StrKeyDef( "sysdSLc", "_SYSTEMD_SLICE" ),                                 # id?
            StrKeyDef( "slnxCtx", "_SELINUX_CONTEXT" ),                               # id?
            StrKeyDef( "uID", "_UID" ),                                               # id?
            StrKeyDef( "cur", "__CURSOR" )
        ])
        self.new_keygroup_with_keys("ids", [
            "sysUnit",
            "usrUnit",
            "udSName",
            "udDvNd",
            "krSubSys",
            "tID",
            "slID",
            "usrInvID",
            "nmDev"
            "glbDom"
            "jbID",
            "invID",
            "sunit",
            "souid",
            "invID",
            "msgID",
            "slPID",
            "sysdUsrUnit",
            "ssysdUwnUID",
            "strmID",
            "exe",
            "sysdSLc",
            "sysdInvID",
            "slnxCtx",
            "uID"
        ])


    def read_json(self: Self, filepath: str):
        #   try:

        line_num: int = 0
        read_len: int = 0
        file_size: int = os.path.getsize(filepath)
        bar = Bar("Processing", max=file_size)
        with open(filepath) as file:
            for line in file:
                read_len += len(line)
                field_dict = json.loads(line)
                self.process_fields(field_dict, line_num)
                bar.next(read_len )
        bar.finish()

if __name__ == "__main__":
    key_graph = JsonLogKeyGraph( "/home/richard/jctl-logs/" )






