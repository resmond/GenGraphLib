from typing import Self

from .ProcLib import ProcBase
from ..graph.KeyValueSchema import KeyValueSchema
from ..bootlog.BootLogManager import BootLogManager

class StreamSinkProc(ProcBase):

    def __init__(self: Self, keyval_schema: KeyValueSchema, bootlog_manager: BootLogManager, queue_size: int | None = None ) -> None:
        super(StreamSinkProc, self).__init__("log_sink", queue_size)
        self.keyval_schema = keyval_schema
        self.bootlog_manager = bootlog_manager

    def start( self: Self ) -> None:
        pass

    def main_loop(self: Self) -> None:
        pass
