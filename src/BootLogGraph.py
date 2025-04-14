from typing import Self

from gengraphlib import (
    KeyValTypes,
    KeyDefBase,
    StrKeyDef,
    IntKeyDef,
    BoolKeyDef,
    TmstKeyDef,
    KeyDict,
    KeySchemaBase,
    BootLogManager,
)
class BootLogGraph( KeySchemaBase ):
    instance: Self | None = None

    def __init__( self: Self, id: str, _log_root: str ) -> None:
        super().__init__( id="1", root_dir = _log_root )
        BootLogGraph.instance = self
        self.log_manager: BootLogManager = BootLogManager( _log_root )
        self._log_keys: KeyDict = KeyDict()

        self.add_keydefs(
            [
                StrKeyDef("priority", "PRIORITY", "evt"),
                StrKeyDef("facility", "SYSLOG_FACILITY", "evt"),
                StrKeyDef("comm", "_COMM", "evt"),
                StrKeyDef("subsystem", "_KERNEL_SUBSYSTEM", "evt"),
                StrKeyDef("device", "_KERNEL_DEVICE", ""),
                StrKeyDef("dev", "DEVICE", ""),
                #
                StrKeyDef("rttime", "__REALTIME_TIMESTAMP", ""),
                StrKeyDef("logtime", "SYSLOG_TIMESTAMP", "evt"),
                #
                StrKeyDef("cmdline", "_CMDLINE", "evt"),
                StrKeyDef("command", "COMMAND", "evt"),
                StrKeyDef("exe", "_EXE", "evt"),
                StrKeyDef("cfgfile", "CONFIG_FILE", ""),
                StrKeyDef("codefn", "CODE_FUNC", ""),
                StrKeyDef("message", "MESSAGE", "evt"),
                #
                StrKeyDef("pid", "_PID", "evt"),
                StrKeyDef("logID", "SYSLOG_IDENTIFIER", "evt"),
                StrKeyDef("logpid", "SYSLOG_PID", "evt"),
                StrKeyDef("linuxctx", "_SELINUX_CONTEXT", "evt"),
                StrKeyDef("cgroup", "_SYSTEMD_CGROUP", "evt"),
                StrKeyDef("userunit", "_SYSTEMD_USER_UNIT", "evt"),
                StrKeyDef("transport", "_TRANSPORT", ""),
                #
                StrKeyDef("bootID", "_BOOT_ID", ""),
                StrKeyDef("seqNum", "__SEQNUM", ""),
                StrKeyDef("mID", "_MACHINE_ID", ""),
                StrKeyDef("hstName", "_HOSTNAME", ""),
                StrKeyDef("mTime", "__MONOTONIC_TIMESTAMP", ""),
                StrKeyDef("rtScope", "_RUNTIME_SCOPE", ""),
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
                StrKeyDef("cdLn", "CODE_LINE", ""),
                StrKeyDef("cdFl", "CODE_FILE", ""),
                StrKeyDef("sysdInvID", "_SYSTEMD_INVOCATION_ID", ""),
                StrKeyDef("sysdSLc", "_SYSTEMD_SLICE", ""),
                StrKeyDef("uID", "_UID", ""),
                StrKeyDef("cur", "__CURSOR", ""),
                StrKeyDef("cap_eff", "_CAP_EFFECTIVE", ""),
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
                StrKeyDef("sysdRaw", "SYSLOG_RAW", ""),
                StrKeyDef("cfgLine", "CONFIG_LINE", ""),
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

    def by_logkey(self: Self, _log_key_str: str) -> KeyDefBase:
        return self._log_keys[_log_key_str]

    def final_init( self ):
        super().final_init()

    def process_field( self: Self, key: str, value: KeyValTypes, rec_num: int, rec_line: str = "" ) -> bool:
        key_def: KeyDefBase | None = self._log_keys.get(key, None)
        if key_def is not None:
            return self.process_keyvalue( key_def, value, rec_num, rec_line )
        else:
            return False

    async def exec_query( self: Self, specific_ndx: int, full_reparse: bool = True ) -> bool:
        #await self.dir_manager.exec( specific_ndx, full_reparse )
        return True

