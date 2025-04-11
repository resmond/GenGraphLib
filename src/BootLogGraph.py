from typing import Self, Any

import json
import os

from progress.bar import Bar

from gengraphlib import (
    process_fields_fn,
    KeyDefBase,
    KeyPropClassSurface,
    StrKeyProp,
    StrKeyDef,
    IntKeyDef, 
    BoolKeyDef,
    TmstKeyDef,
    KeyDefIndex,
    KeyRepository,
    KeyValueTriggerBase,
    AddValueResult,
    BootLogDirBase,
    BootLogManagerBase
)

class GraphLogDir( BootLogDirBase ):
    def __init__( self: Self, root_dir: str, log_rec: str ) -> None:
        super().__init__( root_dir, log_rec )

class GraphLogDirManager( BootLogManagerBase ):

    def __init__( self: Self, root_dir: str, fields_fn: process_fields_fn ) -> None:
        super().__init__( root_dir, fields_fn )
        self._fields_fn = process_fields_fn

class PriorityValueTrigger( KeyValueTriggerBase[str] ):

    def eval( self, value: str ) -> bool:
        if value in ["3", "4", "5", "6", "7"]:
            return True
        else:
            return False

    def gather( self, values: dict[str, str] ) -> dict[str, str]:
        pass

class BootLogGraph( KeyRepository, KeyPropClassSurface ):
    keydefs: list[KeyDefBase] = [
    ]

    def __init__( self: Self, _log_root: str ) -> None:
        super().__init__( _log_root )
        self.dir_manager: GraphLogDirManager = GraphLogDirManager( _log_root, self.process_fields )
        self._log_keys: KeyDefIndex = KeyDefIndex()

        self.priority = StrKeyProp( class_surface = self, key_repository=super(),  _json_key = "priority", _log_key = "PRIORITY", groups=[ "evt" ] )


        self.add_keydefs(
            [
                StrKeyDef("cmdLn", "_CMDLINE", "evt"),
                StrKeyDef("comm", "_COMM", "evt"),
                StrKeyDef("exe", "_EXE", "evt"),
                StrKeyDef("krSubSys", "_KERNEL_SUBSYSTEM", "evt"),
                StrKeyDef("msg", "MESSAGE", "evt"),
                StrKeyDef("pID", "_PID", "evt"),
#                StrKeyDef("priority", "PRIORITY", ["evt", "priority"]),
                StrKeyDef("slID", "SYSLOG_IDENTIFIER", "evt"),
                StrKeyDef("slnxCtx", "_SELINUX_CONTEXT", "evt"),
                StrKeyDef("slPID", "SYSLOG_PID", "evt"),
                StrKeyDef("slTime", "SYSLOG_TIMESTAMP", "evt"),
                StrKeyDef("sysdCgrp", "_SYSTEMD_CGROUP", "evt"),
                StrKeyDef("sysdUsrUnit", "_SYSTEMD_USER_UNIT", "evt"),
                StrKeyDef("sysFac", "SYSLOG_FACILITY", "evt"),
                StrKeyDef("bootID", "_BOOT_ID", ""),
                StrKeyDef("seqNum", "__SEQNUM", ""),
                StrKeyDef("mID", "_MACHINE_ID", ""),
                StrKeyDef("hstName", "_HOSTNAME", ""),
                StrKeyDef("trns", "_TRANSPORT", ""),
                StrKeyDef("mTime", "__MONOTONIC_TIMESTAMP", ""),
                StrKeyDef("rtScope", "_RUNTIME_SCOPE", ""),
                StrKeyDef("krnDev", "_KERNEL_DEVICE", ""),
                StrKeyDef("snID", "__SEQNUM_ID", ""),
                StrKeyDef("rtTime", "__REALTIME_TIMESTAMP", ""),
                StrKeyDef("usrUnit", "UNIT", ""),
                StrKeyDef("udSName", "_UDEV_SYSNAME", ""),
                StrKeyDef("udDvNd", "_UDEV_DEVNODE", ""),
                IntKeyDef("tID", "TID", ""),
                TmstKeyDef("srTime", "_SOURCE_REALTIME_TIMESTAMP", ""),
                BoolKeyDef("lnBk", "_LINE_BREAK", ""),
                StrKeyDef("usrInvID", "USER_INVOCATION_ID", ""),
                StrKeyDef("glbLogApi", "GLIB_OLD_LOG_API", ""),
                StrKeyDef("nmDev", "NM_DEVICE", ""),
                StrKeyDef("glbDom", "GLIB_DOMAIN", ""),
                StrKeyDef("nmLogLev", "NM_LOG_LEVEL", ""),
                StrKeyDef("jbRes", "JOB_RESULT", ""),
                StrKeyDef("smTime", "_SOURCE_MONOTONIC_TIMESTAMP", ""),
                StrKeyDef("jbID", "JOB_ID", ""),
                StrKeyDef("jbType", "JOB_TYPE", ""),
                StrKeyDef("invID", "INVOCATION_ID", ""),
                StrKeyDef("msgID", "MESSAGE_ID", ""),
                StrKeyDef("ssysdUwnUID", "_SYSTEMD_OWNER_UID", ""),
                StrKeyDef("strmID", "_STREAM_ID", ""),
                StrKeyDef("audSes", "_AUDIT_SESSION", ""),
                StrKeyDef("cdFn", "CODE_FUNC", ""),
                StrKeyDef("cdLn", "CODE_LINE", ""),
                StrKeyDef("cdFl", "CODE_FILE", ""),
                StrKeyDef("sysdInvID", "_SYSTEMD_INVOCATION_ID", ""),
                StrKeyDef("sysdSLc", "_SYSTEMD_SLICE", ""),
                StrKeyDef("uID", "_UID", ""),
                StrKeyDef("cur", "__CURSOR", ""),
                StrKeyDef("cap_eff", "_CAP_EFFECTIVE", ""),
                StrKeyDef("sysdCgrp", "_SYSTEMD_CGROUP", "evt"),
                StrKeyDef("gID", "_GID", ""),
                StrKeyDef("avPrty", "AVAILABLE_PRETTY", ""),
                StrKeyDef("muPrty", "MAX_USE_PRETTY", ""),
                StrKeyDef("dskKpfree", "DISK_KEEP_FREE", ""),
                StrKeyDef("dskAvlPrty", "DISK_AVAILABLE_PRETTY", ""),
                StrKeyDef("maxUse", "MAX_USE", ""),
                StrKeyDef("curUse", "CURRENT_USE", ""),
                StrKeyDef("limit", "LIMIT", ""),
                StrKeyDef("limPrty", "LIMIT_PRETTY", ""),
                StrKeyDef("jrnlPath", "JOURNAL_PATH", ""),
                StrKeyDef("jrnlName", "JOURNAL_NAME", ""),
                StrKeyDef("avail", "AVAILABLE", ""),
                StrKeyDef("dslAvail", "DISK_AVAILABLE", ""),
                StrKeyDef("usePrty", "CURRENT_USE_PRETTY", ""),
                StrKeyDef("dskKpFrPrty", "DISK_KEEP_FREE_PRETTY", ""),
                StrKeyDef("where", "WHERE", ""),
                StrKeyDef("dev", "DEVICE", ""),
                StrKeyDef("sysdRaw", "SYSLOG_RAW", ""),
                StrKeyDef("cfgLine", "CONFIG_LINE", ""),
                StrKeyDef("cfgFile", "CONFIG_FILE", ""),
                StrKeyDef("taint", "TAINT", ""),
                StrKeyDef("thID", "THREAD_ID", ""),
                StrKeyDef("tmstBoot", "TIMESTAMP_BOOTTIME", ""),
                StrKeyDef("nmLogDom", "NM_LOG_DOMAINS", ""),
                StrKeyDef("tmstMon", "TIMESTAMP_MONOTONIC", ""),
                StrKeyDef("seatID", "SEAT_ID", ""),
                StrKeyDef("boltVer", "BOLT_VERSION", ""),
                StrKeyDef("boltLogCtx", "BOLT_LOG_CONTEXT", ""),
                StrKeyDef("boltTopic", "BOLT_TOPIC", ""),
                StrKeyDef("boltDomUid", "BOLT_DOMAIN_UID", ""),
                StrKeyDef("boltDomNm", "BOLT_DOMAIN_NAME", ""),
                StrKeyDef("errMsg", "ERROR_MESSAGE", ""),
                StrKeyDef("errCode", "ERROR_CODE", ""),
                StrKeyDef("errDom", "ERROR_DOMAIN", ""),
                StrKeyDef("boltDevNm", "BOLT_DEVICE_NAME", ""),
                StrKeyDef("boltDevSt", "BOLT_DEVICE_STATE", ""),
                StrKeyDef("boltDevUid", "BOLT_DEVICE_UID", ""),
                StrKeyDef("interface", "INTERFACE", ""),
                StrKeyDef("krnUSec", "KERNEL_USEC", ""),
                StrKeyDef("usrUSec", "USERSPACE_USEC", ""),
                StrKeyDef("sesID", "SESSION_ID", ""),
                StrKeyDef("leader", "LEADER", ""),
                StrKeyDef("usrID", "USER_ID", ""),
                StrKeyDef("audLogUid", "_AUDIT_LOGINUID", ""),
                StrKeyDef("sysdUsrSlice", "_SYSTEMD_USER_SLICE", ""),
                StrKeyDef("errNo", "ERRNO", ""),
                StrKeyDef("usrUnit", "USER_UNIT", ""),
                StrKeyDef("sysdSess", "_SYSTEMD_SESSION", ""),
                StrKeyDef("topic", "TOPIC", ""),
                StrKeyDef("command", "COMMAND", "evt"),
                StrKeyDef("exitCd", "EXIT_CODE", ""),
                StrKeyDef("exitSt", "EXIT_STATUS", ""),
                StrKeyDef("unitRes", "UNIT_RESULT", ""),
                StrKeyDef("cpuUseNsec", "CPU_USAGE_NSEC", ""),
                StrKeyDef("memSwapPk", "MEMORY_SWAP_PEAK", ""),
                StrKeyDef("memPk", "MEMORY_PEAK", ""),
                StrKeyDef("bootUSec", "BOOTTIME_USEC", ""),
                StrKeyDef("rtUSec", "REALTIME_USEC", ""),
                StrKeyDef("monUSec", "MONOTONIC_USEC", ""),
                StrKeyDef("nRestarts", "N_RESTARTS", ""),
                StrKeyDef("operator", "OPERATOR", ""),
                StrKeyDef("action", "ACTION", ""),
                StrKeyDef("shutdown", "SHUTDOWN", ""),
                StrKeyDef("nmConn", "NM_CONNECTION", ""),
            ]
        )

        self.define_keygroups(
            [
                ("evt", "Tracked Events"),
                ("skip", "Ignore")
                #("int", "Interesting"),
                #("tm", "Time"),
            ]
        )

        super().init_repository()

    def keyprops_init( self ):
        super().keyprops_init()

    def final_init( self ):
        pass

        # priority_keydef: KeyPropBase[str] = self.get_typed_keyprop("priority")
        # if priority_keydef is not None:
        #     value_trigger = PriorityValueTrigger()
        #     priority_keydef.add_trigger( value_trigger )

    def keyvalue_trigger( self: Self, val_result: KeyValueTriggerBase ) -> AddValueResult:
        return val_result

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

