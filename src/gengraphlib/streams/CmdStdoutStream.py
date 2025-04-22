from pydoc import replace
from typing import Self

from collections.abc import AsyncGenerator

import asyncio as aio
import asyncio.subprocess as asub

class CmdStdoutStream:

    def __init__(self: Self, cmd: str ):
        self.cmd: str = cmd

    async def line_stream( self: Self ) -> AsyncGenerator[ bytes, None ]:
        if self.cmd is None:
            print("CmdChainSource.pipe(): No command")
            return

        exec_process: asub.Process = await aio.create_subprocess_shell( cmd=self.cmd, stdout=aio.subprocess.PIPE, limit = 50*1024 )

        if exec_process is None:
            return

        print("beginnig stdout.read() - loop")


        while True:
            try:
                buffer = await exec_process.stdout.read()
                yield buffer
            except Exception as exc:
                print(exc)


