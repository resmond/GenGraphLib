import asyncio as aio
from typing import Self

from BootLogGraph import BootLogGraph
from src.gengraphlib.proc import AppProcessBase


class MainAppProc( AppProcessBase ):
    def __init__(self: Self):
        super(MainAppProc, self).__init__()

    def init_internals( self: Self ) -> None:
        self.keyval_schema = BootLogGraph( id="1", _log_root = "/home/richard/data/jctl-logs/" )
        super().init_internals()

    async def start(self: Self) -> bool:
        return await super().start()

if __name__ == "__main__":
    print("starting MainAppProc")
    app = MainAppProc()
    ret = aio.run( app.start() )
