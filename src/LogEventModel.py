from typing import Self

from enum import IntEnum

from gengraphlib.model import (
    StrModProp,
    IntEnumModProp,
    ParentModProp,
    TmstModProp,
    ModelInfo,
    DataTableModel
)

class PriorityEnum(IntEnum):
    Info       =    3
    Warning    =    4
    Error      =    5
    Fatal      =    6
    Harmfull   =    7

class PriorityModProp( IntEnumModProp[ PriorityEnum ] ):
    def __init__( self: Self, alias: str, *args, **kwargs ) -> None:
        super().__init__( alias=alias, *args, *kwargs )

class LogEventModel(DataTableModel):
    model = ModelInfo("logevents")

    #priority     = PriorityModProp( alias="PRIORITY")
    timestamp    = TmstModProp(alias="__REALTIME_TIMESTAMP")
    message      = StrModProp(alias="MESSAGE")

    facility     = ParentModProp( alias= "SYSLOG_FACILITY" )
    comm         = ParentModProp( alias= "_COMM" )
    subsystem    = ParentModProp( alias= "_KERNEL_SUBSYSTEM" )
    kerneldevice = ParentModProp( alias= "_KERNEL_DEVICE" )
    device       = ParentModProp( alias= "DEVICE" )

    cfgfile      = ParentModProp( alias= "CONFIG_FILE" )
    cmdline      = StrModProp(alias="_CMDLINE")
    command      = StrModProp(alias="COMMAND")
    exe          = StrModProp(alias="_EXE")
    code_fn      = StrModProp(alias="CODE_FUNC")
    code_line    = StrModProp(alias="CODE_LINE")
    code_file    = StrModProp(alias="CODE_FILE")

    def __init__( self: Self ) -> None:
        super().__init__("logevent")








