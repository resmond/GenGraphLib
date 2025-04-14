from src.gengraphlib import StrKeyDef


class LogDataVector:

    rt_time    = StrKeyDef("rt_time", "__REALTIME_TIMESTAMP", "evt")
    log_time   = StrKeyDef("log_time", "SYSLOG_TIMESTAMP", "evt")

    priority   = StrKeyDef("priority", "PRIORITY", "evt")

    transport  = StrKeyDef("transport", "_TRANSPORT", "evt"),
    facility   = StrKeyDef("facility", "SYSLOG_FACILITY", "evt")
    comm       = StrKeyDef("comm", "_COMM", "evt")
    subsystem  = StrKeyDef("subsystem", "_KERNEL_SUBSYSTEM", "evt")
    device     = StrKeyDef("device", "_KERNEL_DEVICE", "")
    dev        = StrKeyDef("dev", "DEVICE", "evt")

    pid        = StrKeyDef("pid", "_PID", "evt")
    log_id     = StrKeyDef("log_id", "SYSLOG_IDENTIFIER", "evt"),
    log_pid    = StrKeyDef("log_pid", "SYSLOG_PID", "evt"),
    linuxctx   = StrKeyDef("linuxctx", "_SELINUX_CONTEXT", "evt"),
    cgroup     = StrKeyDef("cgroup", "_SYSTEMD_CGROUP", "evt"),
    user_unit  = StrKeyDef("user_unit", "_SYSTEMD_USER_UNIT", "evt"),

    cmdline    = StrKeyDef("cmdline", "_CMDLINE", "evt")
    command    = StrKeyDef("command", "COMMAND", "evt")
    exe        = StrKeyDef("exe", "_EXE", "evt")

    cfgfile    = StrKeyDef("cfgfile", "CONFIG_FILE", "evt")

    code_fn    = StrKeyDef("codefn", "CODE_FUNC", "evt")

    message    = StrKeyDef("message", "MESSAGE", "evt")

