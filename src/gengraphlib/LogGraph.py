from typing import Self

import asyncio as aio

import json
import os

from progress.bar import Bar

from .logs.KeyGraphBase import KeyGraphBase, StrKeyDef, IntKeyDef, BoolKeyDef, TmstKeyDef, process_fields_fn
from .logs.BootLogDirBase import BootLogDirBase
from .logs.LogDirManagerBase import LogDirManagerBase, GraphCmd

class GraphLogDir( BootLogDirBase ):
    def __init__(self: Self, root_dir: str, log_line: str, fields_fn: process_fields_fn ) -> None:
        super( GraphLogDir, self ).__init__( root_dir, log_line )

class GraphLogDirManager( LogDirManagerBase ):

    def __init__( self: Self, root_dir: str, fields_fn: process_fields_fn ) -> None:
        self._fields_fn = process_fields_fn
        super( GraphLogDirManager, self ).__init__( root_dir, fields_fn )

class LogGraph( KeyGraphBase ):
    def __init__( self: Self, _log_root: str ) -> None:
        super( LogGraph, self ).__init__( _log_root )
        self.dir_manager: GraphLogDirManager = GraphLogDirManager( _log_root, self.process_fields )
        self.add_keydefs([
            StrKeyDef( "bootID", "_BOOT_ID"),
            StrKeyDef( "seqNum", "__SEQNUM" ),
            StrKeyDef( "mID", "_MACHINE_ID" ),
            StrKeyDef( "hstName", "_HOSTNAME" ),
            StrKeyDef( "trns", "_TRANSPORT" ),
            StrKeyDef( "mTime", "__MONOTONIC_TIMESTAMP" ),
            StrKeyDef( "priority", "PRIORITY" ),
            StrKeyDef( "msg", "MESSAGE" ),
            StrKeyDef( "rtScope", "_RUNTIME_SCOPE" ),
            StrKeyDef( "krnDev", "_KERNEL_DEVICE" ),
            StrKeyDef( "snID", "__SEQNUM_ID" ),                                       # id
            StrKeyDef( "rtTime", "__REALTIME_TIMESTAMP"),                             # id
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
            StrKeyDef( "cur", "__CURSOR" ),
            StrKeyDef( "cap_eff", "_CAP_EFFECTIVE" ),
            StrKeyDef( "pID", "_PID" ),                                               # id
            StrKeyDef( "sysdCgrp","_SYSTEMD_CGROUP" ),                                # id
            StrKeyDef( "gID","_GID" ),                                                # id
            StrKeyDef( "avPrty","AVAILABLE_PRETTY" ),
            StrKeyDef( "muPrty","MAX_USE_PRETTY" ),
            StrKeyDef( "dskKpfree","DISK_KEEP_FREE" ),
            StrKeyDef( "dskAvlPrty","DISK_AVAILABLE_PRETTY" ),
            StrKeyDef( "maxUse","MAX_USE" ),
            StrKeyDef( "curUse","CURRENT_USE" ),
            StrKeyDef( "limit","LIMIT" ),
            StrKeyDef( "limPrty","LIMIT_PRETTY" ),
            StrKeyDef( "jrnlPath","JOURNAL_PATH" ),
            StrKeyDef( "jrnlName","JOURNAL_NAME" ),
            StrKeyDef( "avail","AVAILABLE" ),
            StrKeyDef( "dslAvail","DISK_AVAILABLE" ),
            StrKeyDef( "","CURRENT_USE_PRETTY" ),
            StrKeyDef( "dskKpFrPrty","DISK_KEEP_FREE_PRETTY" ),
            StrKeyDef( "where","WHERE" ),
            StrKeyDef( "dev","DEVICE" ),                                             # id
            StrKeyDef( "sysdRaw","SYSLOG_RAW" ),
            StrKeyDef( "cfgLine","CONFIG_LINE" ),
            StrKeyDef( "cfgFile","CONFIG_FILE" )
        ])
        self.new_keygroup_with_keys("ids", [
            "cfgLine",
            "cfgFile",
            "dev",
            "sysdCgrp",
            "gID",
            "pID",
            "rtScope",
            "krnDev",
            "rtTime",
            "sysUnit",
            "usrUnit",
            "udSName",
            "udDvNd",
            "krSubSys",
            "snID",
            "tID",
            "slID",
            "usrInvID",
            "nmDev",
            "glbDom",
            "jbID",
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
        try:
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
        except FileNotFoundError as ext:
            print(f'[JsonLogKeyGraph.read_json]FileNotFoundError: {ext} - {filepath}')

    async def exec_query( self: Self, exec_cmd: GraphCmd, specific_ndx: int ) -> bool:
        await self.dir_manager.exec( exec_cmd, specific_ndx )
        return True

"""
    def read_json(self: Self, filepath: str):
        try:
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
        except FileNotFoundError as ext:
            print(f'[JsonLogKeyGraph.read_json]FileNotFoundError: {ext} - {filepath}')

    async def parse_stream( self: Self ) -> bool:

        return True
"""

if __name__ == "__main__":
    print("[LogGraph] starting main")

#    try:
    log_root: str = "/home/richard/data/jctl-logs"
    key_graph = LogGraph( log_root )
    aio.run( key_graph.exec_query( GraphCmd.Full, 1 ) )

#    except Exception as e:
#        print(f"[LodDirManager] Exception: {e}")

    print("[LogGraph] done")
