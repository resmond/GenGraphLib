from typing import Self, Any

import json
import os

from progress.bar import Bar

from .graph.KeyDefs import (
    KeyDefBase,
    StrKeyDef,
    IntKeyDef,
    BoolKeyDef,
    TmstKeyDef,
    process_fields_fn,
)

from .bootlog.BootLogDirBase import BootLogDirBase
from .bootlog.BootLogManagerBase import BootLogManagerBase
from .graph.KeyRepository import KeyDefIndex, KeyRepository

class GraphLogDir( BootLogDirBase ):
    def __init__( self: Self, root_dir: str, log_rec: str ) -> None:
        super( GraphLogDir, self ).__init__( root_dir, log_rec )

class GraphLogDirManager( BootLogManagerBase ):

    def __init__( self: Self, root_dir: str, fields_fn: process_fields_fn ) -> None:
        self._fields_fn = process_fields_fn
        super( GraphLogDirManager, self ).__init__( root_dir, fields_fn )

class BootLogGraph( KeyRepository ):
    keydefs: list[KeyDefBase] = [
    ]



    def __init__( self: Self, _log_root: str ) -> None:
        self.dir_manager: GraphLogDirManager = GraphLogDirManager( _log_root, self.process_fields )
        self._log_keys: KeyDefIndex = KeyDefIndex()
        super( BootLogGraph, self ).__init__( _log_root )

        self.add_keydefs([
            StrKeyDef("bootID", "_BOOT_ID", "sid"),                     # sid
            StrKeyDef("seqNum", "__SEQNUM", "sid"),
            StrKeyDef("mID", "_MACHINE_ID", "sid"),
            StrKeyDef("hstName", "_HOSTNAME", "sid"),
            StrKeyDef("trns", "_TRANSPORT", "hdr"),                     # hdr
            StrKeyDef("mTime", "__MONOTONIC_TIMESTAMP", "tm"),          # tm
            StrKeyDef("priority", "PRIORITY", "hdr"),
            StrKeyDef("msg", "MESSAGE","evt"),                          # evt
            StrKeyDef("rtScope", "_RUNTIME_SCOPE", "hdr"),
            StrKeyDef("krnDev", "_KERNEL_DEVICE", "id"),                # id
            StrKeyDef("snID", "__SEQNUM_ID", "id"),
            StrKeyDef("rtTime", "__REALTIME_TIMESTAMP", "tm"),
            StrKeyDef("sysUnit", "_SYSTEMD_UNIT", "id"),
            StrKeyDef("usrUnit", "UNIT", "id"),
            StrKeyDef("udSName", "_UDEV_SYSNAME", "id"),
            StrKeyDef("udDvNd", "_UDEV_DEVNODE", "id"),
            StrKeyDef("krSubSys", "_KERNEL_SUBSYSTEM", "id"),
            IntKeyDef("tID", "TID", "id"),
            StrKeyDef("comm", "_COMM", "evt"),
            StrKeyDef("slID", "SYSLOG_IDENTIFIER", "id"),
            TmstKeyDef("srTime", "_SOURCE_REALTIME_TIMESTAMP", "tm"),
            StrKeyDef("sysFac", "SYSLOG_FACILITY", "hdr"),
            BoolKeyDef("lnBk", "_LINE_BREAK", "skip"),
            StrKeyDef("cmdLn", "_CMDLINE","cmd"),
            StrKeyDef("usrInvID", "USER_INVOCATION_ID", "id"),
            StrKeyDef("glbLogApi", "GLIB_OLD_LOG_API","glib"),
            StrKeyDef("nmDev", "NM_DEVICE", "nm"),
            StrKeyDef("glbDom", "GLIB_DOMAIN", "glb"),
            StrKeyDef("nmLogLev", "NM_LOG_LEVEL", "nm"),
            StrKeyDef("jbRes", "JOB_RESULT", "job"),
            StrKeyDef("smTime", "_SOURCE_MONOTONIC_TIMESTAMP","tm"),
            StrKeyDef("jbID", "JOB_ID", "job"),
            StrKeyDef("jbType", "JOB_TYPE", "job"),
            StrKeyDef("invID", "INVOCATION_ID", "id"),
            StrKeyDef("slTime", "SYSLOG_TIMESTAMP", "tm"),
            StrKeyDef("msgID", "MESSAGE_ID", "id"),
            StrKeyDef("slPID", "SYSLOG_PID", "id"),
            StrKeyDef("sysdUsrUnit", "_SYSTEMD_USER_UNIT", "sysd"),
            StrKeyDef("ssysdUwnUID", "_SYSTEMD_OWNER_UID", "sysd"),
            StrKeyDef("strmID", "_STREAM_ID", "id"),
            StrKeyDef("audSes", "_AUDIT_SESSION", "aud"),
            StrKeyDef("cdFn", "CODE_FUNC", "cmd"),
            StrKeyDef("cdLn", "CODE_LINE", "cmd"),
            StrKeyDef("cdFl", "CODE_FILE", "cmd"),
            StrKeyDef("sysdInvID", "_SYSTEMD_INVOCATION_ID", "id"),
            StrKeyDef("exe", "_EXE", "id"),
            StrKeyDef("sysdSLc", "_SYSTEMD_SLICE", "id"),
            StrKeyDef("slnxCtx", "_SELINUX_CONTEXT", "id"),
            StrKeyDef("uID", "_UID", "id"),
            StrKeyDef("cur", "__CURSOR", "skip"),
            StrKeyDef("cap_eff", "_CAP_EFFECTIVE", "skip"),
            StrKeyDef("pID", "_PID", "id"),
            StrKeyDef("sysdCgrp", "_SYSTEMD_CGROUP", "id"),
            StrKeyDef("gID", "_GID", "id"),
            StrKeyDef("avPrty", "AVAILABLE_PRETTY", "prty"),
            StrKeyDef("muPrty", "MAX_USE_PRETTY", "prty"),
            StrKeyDef("dskKpfree", "DISK_KEEP_FREE", "dsk"),
            StrKeyDef("dskAvlPrty", "DISK_AVAILABLE_PRETTY", "dsk"),
            StrKeyDef("maxUse", "MAX_USE", "dsk"),
            StrKeyDef("curUse", "CURRENT_USE", "dsk"),
            StrKeyDef("limit", "LIMIT", "dsk"),
            StrKeyDef("limPrty", "LIMIT_PRETTY", "prty"),
            StrKeyDef("jrnlPath", "JOURNAL_PATH", "jrnl"),
            StrKeyDef("jrnlName", "JOURNAL_NAME", "jrnl"),
            StrKeyDef("avail", "AVAILABLE", "dsk"),
            StrKeyDef("dslAvail", "DISK_AVAILABLE", "dsk"),
            StrKeyDef("usePrty", "CURRENT_USE_PRETTY", "prty"),
            StrKeyDef("dskKpFrPrty", "DISK_KEEP_FREE_PRETTY", "dsk"),
            StrKeyDef("where", "WHERE", "unkn"),
            StrKeyDef("dev", "DEVICE", "id"),
            StrKeyDef("sysdRaw", "SYSLOG_RAW", "dsk"),
            StrKeyDef("cfgLine", "CONFIG_LINE", "cmd"),
            StrKeyDef("cfgFile", "CONFIG_FILE", "cmd"),
            StrKeyDef("taint","TAINT", "unkn" ),
            StrKeyDef("thID","THREAD_ID", "id" ),
            StrKeyDef("tmstBoot","TIMESTAMP_BOOTTIME", "tm" ),
            StrKeyDef("nmLogDom","NM_LOG_DOMAINS", "nm" ),
            StrKeyDef("tmstMon","TIMESTAMP_MONOTONIC", "tm" ),
            StrKeyDef("seatID","SEAT_ID", "id" ),
            StrKeyDef("boltVer","BOLT_VERSION", "bolt" ),
            StrKeyDef("boltLogCtx","BOLT_LOG_CONTEXT", "bolt" ),
            StrKeyDef("boltTopic","BOLT_TOPIC", "bolt"  ),
            StrKeyDef("boltDomUid","BOLT_DOMAIN_UID", "bolt" ),
            StrKeyDef("boltDomNm","BOLT_DOMAIN_NAME", "bolt" ),
            StrKeyDef("errMsg","ERROR_MESSAGE", "err" ),
            StrKeyDef("errCode","ERROR_CODE", "err" ),
            StrKeyDef("errDom","ERROR_DOMAIN", "err" ),
            StrKeyDef("boltDevNm","BOLT_DEVICE_NAME", "bolt" ),
            StrKeyDef("boltDevSt","BOLT_DEVICE_STATE", "bolt" ),
            StrKeyDef("boltDevUid","BOLT_DEVICE_UID", "bolt" ),
            StrKeyDef("interface","INTERFACE", "hdr" ),
            StrKeyDef("krnUSec","KERNEL_USEC", "tm" ),
            StrKeyDef("usrUSec","USERSPACE_USEC", "tm" ),
            StrKeyDef("sesID","SESSION_ID", "id" ),
            StrKeyDef("leader","LEADER", "unkn" ),
            StrKeyDef("usrID","USER_ID", "id" ),
            StrKeyDef("audLogUid","_AUDIT_LOGINUID", "aud" ),
            StrKeyDef("sysdUsrSlice","_SYSTEMD_USER_SLICE", "id" ),
            StrKeyDef("errNo","ERRNO", "err" ),
            StrKeyDef("usrUnit","USER_UNIT", "id" ),
            StrKeyDef("sysdSess","_SYSTEMD_SESSION", "id" ),
            StrKeyDef("topic","TOPIC", "unkn" ),
            StrKeyDef("command","COMMAND", "cmd" ),
            StrKeyDef("exitCd","EXIT_CODE", "unkn" ),
            StrKeyDef("exitSt","EXIT_STATUS", "unkn" ),
            StrKeyDef("unitRes","UNIT_RESULT", "unkn" ),
            StrKeyDef("cpuUseNsec","CPU_USAGE_NSEC", "dsk" ),
            StrKeyDef("memSwapPk","MEMORY_SWAP_PEAK", "dsk" ),
            StrKeyDef("memPk","MEMORY_PEAK", "dsk" ),
            StrKeyDef("bootUSec","BOOTTIME_USEC", "tm" ),
            StrKeyDef("rtUSec","REALTIME_USEC", "tm" ),
            StrKeyDef("monUSec","MONOTONIC_USEC", "tm" ),
            StrKeyDef("nRestarts","N_RESTARTS", "op" ),
            StrKeyDef("operator","OPERATOR", "unkn" ),
            StrKeyDef("action","ACTION", "op" ),
            StrKeyDef("shutdown","SHUTDOWN", "op" ),
            StrKeyDef("nmConn","NM_CONNECTION", "nm" )
        ])

        self.define_keygroups([
            ("id", "ID"),
            ("tm", "Time"),
            ("hdr", "Header"),
            ("evt", "Event"),
            ("cmd", "Command"),
            ("sysd", "SYSTEMD"),
            ("skip", "Ignore"),
            ("glib", "Glib"),
            ("nm", "nmRelated"),
            ("job", "JobRelated"),
            ("aud", "Audit"),
            ("prty", "Pretty"),
            ("dsk", "Resources"),
            ("jrnl", "Journal"),
            ("bolt", "BOLT"),
            ("err", "ERROR"),
            ("op", "Operations"),
            ("unkn", "Unknown")
        ])

        self.init_repository()

    def by_logkey(self: Self, _log_key_str: str) -> KeyDefBase:
        return self._log_keys[_log_key_str]

    def process_field( self: Self, key: str, value: Any, line_num: int, log_line: str = "" ) -> bool:
        key_def: KeyDefBase | None = self._log_keys.get(key, None)
        if key_def is not None:
            return self.process_keyvalue( key_def, value, line_num, log_line )
        else:
            return False

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

    async def exec_query( self: Self, specific_ndx: int, full_reparse: bool = True ) -> bool:
        await self.dir_manager.exec( specific_ndx, full_reparse )
        return True

"""
        self.new_keygroup_with_keys("ids", [
            "sysdUsrSlice",
            "usrUnit",
            "sysdSess",
            "usrID",
            "sesID",
            "seatID",
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

"""
