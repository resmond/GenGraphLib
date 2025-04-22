from typing import Self
import multiprocessing as mp

from gengraphlib import (
    KeyDefBase,
    StrKeyDef,
    IntKeyDef,
    BoolKeyDef,
    TmstKeyDef,
    KeyDict,
    KeyValueSchema,
    BootLogManager,
    ValuePumpTask,
    StreamSourceTask,
    BootLogDir,
    IndexManagerTask
)

class ParseProcessInfo:
    def __init__( self: Self, app_msgqueue: mp.Queue, id: str, log_root: str, boot_index: int, write_bin: bool, write_log: bool ) -> None:
        self.app_msgqueue: mp.Queue = app_msgqueue

        self.id: str         = id
        self.log_root: str   = log_root
        self.boot_index: int = boot_index
        self.write_bin: bool = write_bin
        self.write_log: bool = write_log

class BootLogSchema( KeyValueSchema ):

    @staticmethod
    def entrypoint( parse_info: ParseProcessInfo ) -> None:
        BootLogSchema( parse_info )

    def __init__( self: Self, parse_info: ParseProcessInfo ) -> None:
        super( BootLogSchema, self ).__init__( id=parse_info.id, root_dir = parse_info.log_root )

        self.id: str = parse_info.id
        self.log_root: str = parse_info.log_root
        self.boot_index: int = parse_info.boot_index
        self.write_bin: bool = parse_info.write_bin
        self.write_log: bool = parse_info.write_log

        self.app_msgqueue: mp.Queue = parse_info.app_msgqueue

        self.log_manager:          BootLogManager        = BootLogManager( parse_info.log_root )
        self._log_keys:            KeyDict               = KeyDict()
        self.cnt: int = 0

        self.journal_streamsource: StreamSourceTask | None = None
        self.indexmanager_task: IndexManagerTask | None = None
        self.valuepump_task: ValuePumpTask | None = None
        self.bootlog_dir: BootLogDir | None = None
        self.active_keys: set[str] | None = None
        self.record_queues: mp.Queue | None = None

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

        super().init_repository()

    # noinspection PyTypeChecker
    def by_logkey(self: Self, _log_key_str: str) -> KeyDefBase:
        return self._log_keys[_log_key_str]

    def final_init( self ):
        self.launch_processing()

    def get_activekeys( self, group_id: str ) -> set[str]:
        return { keydef.alias for key, keydef in self.items() if keydef.in_group(group_id) }

    def launch_processing( self: Self ) -> None:

        self.active_keys = self.get_activekeys( "evt" )
        self.bootlog_dir = self.log_manager.get_bootlogdir( boot_index = self.boot_index )
        self.valuepump_task = ValuePumpTask( self )
        self.indexmanager_task = IndexManagerTask(self, self.log_root )


        self.indexmanager_task.init_indexes( self.active_keys )
        self.record_queues = self.valuepump_task.init_queues( self.indexmanager_task )
        self.journal_streamsource = StreamSourceTask( self, self.active_keys, self.record_queues )

        self.indexmanager_task.start_indexes()
        self.valuepump_task.start()
        
        self.journal_streamsource.launch_processing( bootlogdir = self.bootlog_dir, write_bin=self.write_bin, write_log = self.write_log )


    



