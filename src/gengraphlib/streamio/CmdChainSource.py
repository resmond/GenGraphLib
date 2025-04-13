from typing import Self

from src.gengraphlib import ChainSourceBase, ChainableResult

class CmdChainSource[ T: ChainableResult ](ChainSourceBase[T]):

    def __init__(self, cmd):
        super(CmdChainSource, self).__init__()
        self.cmd = cmd
        from src.gengraphlib import CmdStreamSource
        self.cmd_stream = CmdStreamSource(cmd)

    async def _new_result( self: Self ) -> T | None:
        return None







