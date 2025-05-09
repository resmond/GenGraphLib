from typing import Self

from enum import IntEnum

from gengraphlib.model import (
    StrModProp,
    IntEnumModProp,
    TmstModProp,
    ModelInfo,
    DataTableModel
)

from pyarrow import uint8

class PriorityEnum(IntEnum):
    Info       =    3
    Warning    =    4
    Error      =    5
    Fatal      =    6
    Harmfull   =    7

class PriorityModProp( IntEnumModProp[ PriorityEnum ] ):
    def __init__( self: Self, alias: str, *args, **kwargs ) -> None:
        super().__init__( alias=alias, store_type=uint8(), *kwargs )

    def recv_value( self: Self, row_num: int, import_value: str ) -> None:
        #int_value = int(import_value)
        super().recv_value( row_num, import_value )

    def finalize( self: Self, maxrownum: int ) -> None:
        super().finalize( maxrownum )

class LogEventModel(DataTableModel):
    model = ModelInfo("logevents")

    priority       = PriorityModProp( alias="PRIORITY")
    timestamp      = TmstModProp(alias="__REALTIME_TIMESTAMP")
    sysd_cgroup    = StrModProp(alias="_SYSTEMD_CGROUP")
    syslog_id      = StrModProp(alias="SYSLOG_IDENTIFIER")
    netwk_domains  = StrModProp(alias="NM_LOG_DOMAINS")
    netwk_device   = StrModProp(alias="NM_DEVICE")
    message        = StrModProp(alias="MESSAGE")

    # pid          = StrModProp(alias="_PID")
    # syslog_pid   = StrModProp(alias="SYSLOG_PID")
    # linux_ctx    = StrModProp(alias="_SELINUX_CONTEXT")
    #sysd_usrunit = StrModProp(alias="_SYSTEMD_USER_UNIT")
    # transport    = StrModProp(alias="_TRANSPORT")


    # facility     = ParentModProp( alias= "SYSLOG_FACILITY" )
    # comm         = ParentModProp( alias= "_COMM" )
    # subsystem    = ParentModProp( alias= "_KERNEL_SUBSYSTEM" )
    # kerneldevice = ParentModProp( alias= "_KERNEL_DEVICE" )
    # device       = ParentModProp( alias= "DEVICE" )

    # cfgfile      = ParentModProp( alias= "CONFIG_FILE" )
    # cmdline      = StrModProp(alias="_CMDLINE")
    # command      = StrModProp(alias="COMMAND")
    # exe          = StrModProp(alias="_EXE")
    # code_fn      = StrModProp(alias="CODE_FUNC")
    # code_line    = StrModProp(alias="CODE_LINE")
    # code_file    = StrModProp(alias="CODE_FILE")

    # cursor       = StrModProp(alias="__CURSOR")
    # usrUnit      = StrModProp(alias="UNIT")
    # tID          = StrModProp(alias="TID")
    # usrInvID     = StrModProp(alias="USER_INVOCATION_ID")
    # strmID       = StrModProp(alias="_STREAM_ID")
    # sysdInvID    = StrModProp(alias="_SYSTEMD_INVOCATION_ID")
    # cap_eff      = StrModProp(alias="_CAP_EFFECTIVE")
    # jrnlPath     = StrModProp(alias="JOURNAL_PATH")
    # jrnlName     = StrModProp(alias="JOURNAL_NAME")
    #sysdRaw      = StrModProp(alias="SYSLOG_RAW")
    #thID         = StrModProp(alias="THREAD_ID")
    #errMsg       = StrModProp(alias="ERROR_MESSAGE")
    #errCode      = StrModProp(alias="ERROR_CODE")
    #errDom       = StrModProp(alias="ERROR_DOMAIN")
    #interface    = StrModProp(alias="INTERFACE")



    def __init__( self: Self ) -> None:
        super().__init__()








