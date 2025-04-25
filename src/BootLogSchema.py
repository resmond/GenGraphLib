from typing import Self
import multiprocessing as mp

from gengraphlib import (
    StrKeyDef,
    IntKeyDef,
    BoolKeyDef,
    TmstKeyDef,
    KeyDict,
    KeyValueSchema,
    BootLogManager,
    BootLog,
    BootLogInfo
)

class ParseProcessInfo:
    def __init__( self: Self, app_msgqueue: mp.Queue, end_event: mp.Event, id: str, log_root: str, boot_index: int, groupid: str, autostart: bool = False,  write_bin: bool = False, write_log: bool = False ) -> None:
        self.app_msgqueue: mp.Queue = app_msgqueue
        self.end_event: mp.Event = end_event

        self.id: str         = id
        self.log_root: str   = log_root
        self.boot_index: int = boot_index
        self.groupid:    str = groupid
        self.write_bin: bool = write_bin
        self.write_log: bool = write_log
        self.autostart: bool = autostart

class BootLogSchema( KeyValueSchema ):

    @staticmethod
    def entrypoint( parse_info: ParseProcessInfo ) -> None:
        bootlog_schema = BootLogSchema( parse_info )
        bootlog_schema.launch_indexing( -1, "evt" )

    def __init__( self: Self, parse_info: ParseProcessInfo ) -> None:
        super( BootLogSchema, self ).__init__( id=parse_info.id, root_dir = parse_info.log_root )

        self.cnt:           int  = 0
        self.id:            str  = parse_info.id
        self.log_root:      str  = parse_info.log_root
        self.cur_bootindex: int  = parse_info.boot_index
        self.cur_groupid:   str  = parse_info.groupid
        self.autostart:     bool = parse_info.autostart
        self.write_bin:     bool = parse_info.write_bin
        self.write_log:     bool = parse_info.write_log

        self.app_msgqueue: mp.Queue = parse_info.app_msgqueue
        self.end_event:    mp.Event = parse_info.end_event

        self.log_manager:   BootLogManager | None = None
        self._alias_map:    KeyDict         = KeyDict()

        self.cur_bootlog:       BootLog              | None = None
        self.bootlog_info:      BootLogInfo          | None = None

        self.active_keys:       set[str]             | None = None
        self.queues_byalias:    dict[str, mp.Queue ] | None = None

        self.add_keydefs(
            [
                StrKeyDef("priority", "PRIORITY", "evt"),
                StrKeyDef("facility", "SYSLOG_FACILITY", "evt"),
                StrKeyDef("comm", "_COMM", "evt"),
                StrKeyDef("subsystem", "_KERNEL_SUBSYSTEM", "evt"),
                StrKeyDef("device", "_KERNEL_DEVICE", "evt"),
                StrKeyDef("dev", "DEVICE", "evt"),
                #
                StrKeyDef("rttime", "__REALTIME_TIMESTAMP", "evt"),
                StrKeyDef("logtime", "SYSLOG_TIMESTAMP", "evt"),
                #
                StrKeyDef("cmdline", "_CMDLINE", "evt"),
                StrKeyDef("command", "COMMAND", "evt"),
                StrKeyDef("exe", "_EXE", "evt"),
                StrKeyDef("cfgfile", "CONFIG_FILE", "evt"),
                StrKeyDef("codefn", "CODE_FUNC", "evt"),
                StrKeyDef("message", "MESSAGE", "evt"),
                #
                StrKeyDef("pid", "_PID", "evt"),
                StrKeyDef("logID", "SYSLOG_IDENTIFIER", "evt"),
                StrKeyDef("logpid", "SYSLOG_PID", "evt"),
                StrKeyDef("linuxctx", "_SELINUX_CONTEXT", "evt"),
                StrKeyDef("cgroup", "_SYSTEMD_CGROUP", "evt"),
                StrKeyDef("userunit", "_SYSTEMD_USER_UNIT", "evt"),
                StrKeyDef("transport", "_TRANSPORT", "evt"),
                #
                StrKeyDef("rtScope", "_RUNTIME_SCOPE", "eval"),
                StrKeyDef("udSName", "_UDEV_SYSNAME", "eval"),
                StrKeyDef("udDvNd", "_UDEV_DEVNODE", "eval"),
                StrKeyDef("nmDev", "NM_DEVICE", "eval"),
                StrKeyDef("msgID", "MESSAGE_ID", "eval"),
                StrKeyDef("cdLn", "CODE_LINE", "eval"),
                StrKeyDef("cdFl", "CODE_FILE", "eval"),
                StrKeyDef("sysdSLc", "_SYSTEMD_SLICE", "eval"),
                StrKeyDef("cur", "__CURSOR", "eval"),
                StrKeyDef("cfgLine", "CONFIG_LINE", "eval"),
                # ---
                StrKeyDef("bootID", "_BOOT_ID", "noise"),
                StrKeyDef("seqNum", "__SEQNUM", "noise"),
                StrKeyDef("mID", "_MACHINE_ID", "noise"),
                StrKeyDef("hstName", "_HOSTNAME", "noise"),
                StrKeyDef("mTime", "__MONOTONIC_TIMESTAMP", "noise"),
                StrKeyDef("snID", "__SEQNUM_ID", "noise"),
                StrKeyDef("rtTime", "__REALTIME_TIMESTAMP", "noise"),
                StrKeyDef("usrUnit", "UNIT", "noise"),
                IntKeyDef("tID", "TID", "noise"),
                TmstKeyDef("srTime", "_SOURCE_REALTIME_TIMESTAMP", "noise"),
                BoolKeyDef("lnBk", "_LINE_BREAK", "noise"),
                StrKeyDef("usrInvID", "USER_INVOCATION_ID", "noise"),
                StrKeyDef("glbLogApi", "GLIB_OLD_LOG_API", "noise"),
                StrKeyDef("glbDom", "GLIB_DOMAIN", "noise"),
                StrKeyDef("nmLogLev", "NM_LOG_LEVEL", "noise"),
                StrKeyDef("jbRes", "JOB_RESULT", "noise"),
                StrKeyDef("smTime", "_SOURCE_MONOTONIC_TIMESTAMP", "noise"),
                StrKeyDef("jbID", "JOB_ID", "noise"),
                StrKeyDef("jbType", "JOB_TYPE", "noise"),
                StrKeyDef("invID", "INVOCATION_ID", "noise"),
                StrKeyDef("ssysdUwnUID", "_SYSTEMD_OWNER_UID", "noise"),
                StrKeyDef("strmID", "_STREAM_ID", "noise"),
                StrKeyDef("audSes", "_AUDIT_SESSION", "noise"),
                StrKeyDef("sysdInvID", "_SYSTEMD_INVOCATION_ID", "noise"),
                StrKeyDef("uID", "_UID", "noise"),
                StrKeyDef("cap_eff", "_CAP_EFFECTIVE", "noise"),
                StrKeyDef("gID", "_GID", "noise"),
                StrKeyDef("avPrty", "AVAILABLE_PRETTY", "noise"),
                StrKeyDef("muPrty", "MAX_USE_PRETTY", "noise"),
                StrKeyDef("dskKpfree", "DISK_KEEP_FREE", "noise"),
                StrKeyDef("dskAvlPrty", "DISK_AVAILABLE_PRETTY", "noise"),
                StrKeyDef("maxUse", "MAX_USE", "noise"),
                StrKeyDef("curUse", "CURRENT_USE", "noise"),
                StrKeyDef("limit", "LIMIT", "noise"),
                StrKeyDef("limPrty", "LIMIT_PRETTY", "noise"),
                StrKeyDef("jrnlPath", "JOURNAL_PATH", "noise"),
                StrKeyDef("jrnlName", "JOURNAL_NAME", "noise"),
                StrKeyDef("avail", "AVAILABLE", "noise"),
                StrKeyDef("dslAvail", "DISK_AVAILABLE", "noise"),
                StrKeyDef("usePrty", "CURRENT_USE_PRETTY", "noise"),
                StrKeyDef("dskKpFrPrty", "DISK_KEEP_FREE_PRETTY", "noise"),
                StrKeyDef("where", "WHERE", "noise"),
                StrKeyDef("sysdRaw", "SYSLOG_RAW", "noise"),
                StrKeyDef("taint", "TAINT", "noise"),
                StrKeyDef("thID", "THREAD_ID", "noise"),
                StrKeyDef("tmstBoot", "TIMESTAMP_BOOTTIME", "noise"),
                StrKeyDef("nmLogDom", "NM_LOG_DOMAINS", "noise"),
                StrKeyDef("tmstMon", "TIMESTAMP_MONOTONIC", "noise"),
                StrKeyDef("seatID", "SEAT_ID", "noise"),
                StrKeyDef("boltVer", "BOLT_VERSION", "noise"),
                StrKeyDef("boltLogCtx", "BOLT_LOG_CONTEXT", "noise"),
                StrKeyDef("boltTopic", "BOLT_TOPIC", "noise"),
                StrKeyDef("boltDomUid", "BOLT_DOMAIN_UID", "noise"),
                StrKeyDef("boltDomNm", "BOLT_DOMAIN_NAME", "noise"),
                StrKeyDef("errMsg", "ERROR_MESSAGE", "noise"),
                StrKeyDef("errCode", "ERROR_CODE", "noise"),
                StrKeyDef("errDom", "ERROR_DOMAIN", "noise"),
                StrKeyDef("boltDevNm", "BOLT_DEVICE_NAME", "noise"),
                StrKeyDef("boltDevSt", "BOLT_DEVICE_STATE", "noise"),
                StrKeyDef("boltDevUid", "BOLT_DEVICE_UID", "noise"),
                StrKeyDef("interface", "INTERFACE", "noise"),
                StrKeyDef("krnUSec", "KERNEL_USEC", "noise"),
                StrKeyDef("usrUSec", "USERSPACE_USEC", "noise"),
                StrKeyDef("sesID", "SESSION_ID", "noise"),
                StrKeyDef("leader", "LEADER", "noise"),
                StrKeyDef("usrID", "USER_ID", "noise"),
                StrKeyDef("audLogUid", "_AUDIT_LOGINUID", "noise"),
                StrKeyDef("sysdUsrSlice", "_SYSTEMD_USER_SLICE", "noise"),
                StrKeyDef("errNo", "ERRNO", "noise"),
                StrKeyDef("usrUnit", "USER_UNIT", "noise"),
                StrKeyDef("sysdSess", "_SYSTEMD_SESSION", "noise"),
                StrKeyDef("topic", "TOPIC", "noise"),
                StrKeyDef("exitCd", "EXIT_CODE", "noise"),
                StrKeyDef("exitSt", "EXIT_STATUS", "noise"),
                StrKeyDef("unitRes", "UNIT_RESULT", "noise"),
                StrKeyDef("cpuUseNsec", "CPU_USAGE_NSEC", "noise"),
                StrKeyDef("memSwapPk", "MEMORY_SWAP_PEAK", "noise"),
                StrKeyDef("memPk", "MEMORY_PEAK", "noise"),
                StrKeyDef("bootUSec", "BOOTTIME_USEC", "noise"),
                StrKeyDef("rtUSec", "REALTIME_USEC", "noise"),
                StrKeyDef("monUSec", "MONOTONIC_USEC", "noise"),
                StrKeyDef("nRestarts", "N_RESTARTS", "noise"),
                StrKeyDef("operator", "OPERATOR", "noise"),
                StrKeyDef("action", "ACTION", "noise"),
                StrKeyDef("shutdown", "SHUTDOWN", "noise"),
                StrKeyDef("nmConn", "NM_CONNECTION", "noise"),
            ]
        )

        self.define_keygroups(
            [
                ("evt", "Tracked Events"),
                ("eval", "Interesting"),
                ("noise", "Ignore")
            ]
        )

        self.init_repository()

    def init_repository( self: Self ) -> None:
        super().init_repository()

        self.log_manager = BootLogManager( self.log_root, self.get_schema_info(), self.app_msgqueue, self.end_event )

    def launch_indexing( self: Self, boot_index: int | None = None, group_id: str | None = None ) -> None:

        if boot_index is not None:
            self.cur_bootindex = boot_index

        if group_id is not None:
            self.cur_groupid = group_id

        self.active_keys = self.get_groupkeys( self.cur_groupid )

        self.cur_bootlog  = self.log_manager.get_bootlog( boot_index = self.cur_bootindex )
        self.bootlog_info = self.cur_bootlog.get_info()

        self.cur_bootlog.launch_indexing( self.active_keys, self.write_bin, self.write_log )







    



