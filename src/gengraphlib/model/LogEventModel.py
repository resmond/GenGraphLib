from typing import Self

from enum import IntEnum
import datetime as dt

from . import (
    StrModProp,
    IntEnumModProp,
    BranchModProp,
    TmstModProp,
    ModelRegistry,
    ModelInfo,
    DataTableModel,
    #table_model,
)

class PriorityEnum(IntEnum):
    Info       =    3
    Warning    =    4
    Error      =    5
    Fatal      =    6
    Harmfull   =    7

class PriorityModProp[PriorityEnum](IntEnumModProp):
    def __init__( self: Self, *args, **kwargs ) -> None:
        super().__init__(*args, **kwargs)

#@table_model
class LogEventModel(DataTableModel):
    model_info   = ModelInfo("logevent")

    priority     = PriorityModProp( alias="PRIORITY")
    timestamp    = TmstModProp(alias="__REALTIME_TIMESTAMP")
    message      = StrModProp(alias="MESSAGE")

    facility     = BranchModProp(alias="SYSLOG_FACILITY")
    comm         = BranchModProp(alias="_COMM")
    subsystem    = BranchModProp(alias="_KERNEL_SUBSYSTEM")
    kerneldevice = BranchModProp(alias="_KERNEL_DEVICE")
    device       = BranchModProp(alias="DEVICE")
    cfgfile      = BranchModProp(alias="CONFIG_FILE")

    cmdline      = StrModProp(alias="_CMDLINE")
    command      = StrModProp(alias="COMMAND")
    exe          = StrModProp(alias="_EXE")
    code_fn      = StrModProp(alias="CODE_FUNC")
    code_line    = StrModProp(alias="CODE_LINE")
    code_file    = StrModProp(alias="CODE_FILE")

    def __init__( self: Self ) -> None:
        super().__init__("logevent")

if __name__ == "__main__":

    logevent_model = LogEventModel()

    logevent_model.priority = PriorityEnum.Warning
    subsystem = "device"
    timestamp = dt.date(2025, 5, 1)
    message   = "Trump is really making shit go bad"

    ModelRegistry.init_models()

    ModelRegistry.dump_models()

    def test_fn( x: int, y: int ) -> str:
        return f'x = {x} and y = {y}'

    test = {
        "test": test_fn,
        "other": 25
    }

    print( test["test"]( 5, 8 ) )




