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
    graphmodel,
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

@graphmodel
class LogEventModel:
    model_info = ModelInfo("logevent")

    priority   = PriorityModProp( alias="PRIORITY")
    subsystem  = BranchModProp(alias="_KERNEL_SUBSYSTEM")
    timestamp  = TmstModProp(alias="__REALTIME_TIMESTAMP")
    message    = StrModProp(alias="MESSAGE")




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




