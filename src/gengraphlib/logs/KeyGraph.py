from typing import Self
from enum import IntEnum
from datetime import datetime

KValTypes: type = type[str, int, bool, datetime ]

class KeyType( IntEnum ):
    KStr         = 1
    KInt         = 2
    Kbool        = 3
    KTimeStamp   = 4

class JsonTimestamp:
    def __init__(self: Self, dt_str: str ) -> None:
        dt_val = datetime.fromisoformat(dt_str)
        super(JsonTimestamp, self).__init__(dt_val)

class KeyDef:
    def __init__( self: Self, _json_key: str, _log_key: str, key_type: KeyType = KeyType.KStr, unique: bool = False ) -> None:
        self.json_key: str = _json_key
        self.log_key: str = _log_key
        self.key_type: KeyType = key_type
        self.unique: bool = unique

class KeySet(list[KeyDef]):
    pass

class KeyGroups( dict[str, KeySet ] ):
    def __init__( self: Self, graph_root: dict[str,KeyDef ] ) -> None:
        self.graph_root: dict[str,KeyDef] = graph_root
        super().__init__()

    def add_keygroup( self: Self, keygroup_name: str ) -> None:
        self[ keygroup_name] = list[KeyDef]

    def add_key_to_group( self: Self, _keygroup_name: str, _key_def: KeyDef ) -> None:
        self[_keygroup_name].__setitem__( _key_def.json_key, _key_def )

    def add_keys_to_group( self: Self, _keygroup_name: str, keys: iter( str ) ) -> None:
        for _json_key in keys:
            _key_def = self.graph_root[_json_key]
            self.add_key_to_group( _keygroup_name, _key_def )


keydef_init_list: list[KeyDef] = [
    KeyDef( "sysUnit", "_SYSTEMD_UNIT" ),                                           # 1
    KeyDef( "usrUnit", "UNIT" ),                                                    # 1
    KeyDef( "udSName", "_UDEV_SYSNAME" ),                                           # 1
    KeyDef( "udDvNd", "_UDEV_DEVNODE" ),                                            # 1
    KeyDef( "krSubSys", "_KERNEL_SUBSYSTEM" ),                                      # 1
    KeyDef( "tID", "TID", KeyType.KInt ),                                  # 1
    KeyDef( "comm", "_COMM" ),
    KeyDef( "slID", "SYSLOG_IDENTIFIER" ),                                          # 1
    KeyDef( "srTime", "_SOURCE_REALTIME_TIMESTAMP", KeyType.KTimeStamp ),
    KeyDef( "sysFac", "SYSLOG_FACILITY" ),
    KeyDef( "lnBk", "_LINE_BREAK", KeyType.Kbool ),
    KeyDef( "cmdLn", "_CMDLINE" ),
    KeyDef( "usrInvID", "USER_INVOCATION_ID" ),                            # 1

    KeyDef( "glbLogApi", "GLIB_OLD_LOG_API" ),
    KeyDef( "nmDev", "NM_DEVICE" ),                                        # 1
    KeyDef( "glbDom", "GLIB_DOMAIN" ),                                     # 1
    KeyDef( "nmLogLev", "NM_LOG_LEVEL" ),
    KeyDef( "jbRes", "JOB_RESULT" ),
    KeyDef( "smTime", "_SOURCE_MONOTONIC_TIMESTAMP" ),
    KeyDef( "jbID", "JOB_ID" ),                                            # 1
    KeyDef( "jbType", "JOB_TYPE" ),
    KeyDef( "invID", "INVOCATION_ID" ),                                    # 1
    KeyDef( "slTime", "SYSLOG_TIMESTAMP" ),

    KeyDef( "msgID", "MESSAGE_ID" ),                                       # 1
    KeyDef( "slPID", "SYSLOG_PID" ),                                       # 1
    KeyDef( "sysdUsrUnit", "_SYSTEMD_USER_UNIT" ),                         # 1
    KeyDef( "ssysdUwnUID", "_SYSTEMD_OWNER_UID" ),                         # 1
    KeyDef( "strmID", "_STREAM_ID" ),                                      # 1
    KeyDef( "audSes", "_AUDIT_SESSION" ),
    KeyDef( "cdFn", "CODE_FUNC" ),
    KeyDef( "cdLn", "CODE_LINE" ),
    KeyDef( "cdFl", "CODE_FILE" ),
    KeyDef( "sysdInvID", "_SYSTEMD_INVOCATION_ID" ),                       # 1
    KeyDef( "exe", "_EXE" ),                                               # 1
    KeyDef( "sysdSLc", "_SYSTEMD_SLICE" ),                                 # 1
    KeyDef( "slnxCtx", "_SELINUX_CONTEXT" ),                               # 1
    KeyDef( "uID", "_UID" ),                                               # 1
    KeyDef( "cur", "__CURSOR" )


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



class KeyGraphRoot(dict[str, KeyDef]):
    def __init__(self: Self, root_dir: str) -> None:
        super().__init__()
        self._root_dir = root_dir
        self._log_keys: dict[str,KeyDef] = dict[str,KeyDef]()
        self.key_groups: KeyGroups = KeyGroups(self)

    def by_logkey( self: Self, _log_key_str: str ) -> KeyDef:
        return self._log_keys[_log_key_str]

    def add_keydef( self: Self, _key_def: KeyDef ) -> None:
        self[_key_def.json_key] = _key_def
        self._log_keys[_key_def.log_key] = _key_def

    def add_keydefs( self: Self, _keydefs: list[KeyDef] ) -> None:
        for _key_def in _keydefs:
            self.add_keydef(_key_def)

    def new_keygroup_with_keys( self: Self, _keygroup_name: str, _keys: iter(str) ) -> None:
        self.key_groups.add_keygroup( _keygroup_name )
        self.key_groups.add_key_to_group( _keygroup_name, _keys )


id_keylist: list[str ] = [
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
]

key_graph = KeyGraphRoot( "/home/richard/jctl-logs/" )

key_graph.add_keydefs(keydef_init_list)
key_graph.new_keygroup_with_keys("ids", id_keylist)






