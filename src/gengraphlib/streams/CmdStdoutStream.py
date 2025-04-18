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

        exec_process: asub.Process = await aio.create_subprocess_shell(
            cmd=self.cmd,
            stdout=aio.subprocess.PIPE
        )

        if exec_process is None:
            return

        print("beginnig stdout.read() - loop")
        while True:
            read_buffer = await exec_process.stdout.read( 4096 )
            if read_buffer is None or len(read_buffer) == 0:
                break
            else:
                yield read_buffer

