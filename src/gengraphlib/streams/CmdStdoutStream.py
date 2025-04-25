from typing import Self

from collections.abc import AsyncGenerator

import asyncio as aio
import asyncio.subprocess as asub

class CmdStdoutStream:

    def __init__(self: Self, cmd: str ):
        self.cmd: str = cmd

    async def line_stream( self: Self ) -> AsyncGenerator[ str, None ]:
        if self.cmd is None:
            print("CmdChainSource.pipe(): No command")
            return

        exec_process: asub.Process = await aio.create_subprocess_shell( cmd=self.cmd, stdout=aio.subprocess.PIPE, limit = 16*1024 )

        if exec_process is None:
            return

        print("beginnig stdout.read() - loop")

        while True:
            tail_text: str = ""
            lines: list[str] = []
            try:
                buffer = await exec_process.stdout.read(1024*16)

                new_text = buffer.decode(errors="replace")

                lines = (tail_text + new_text).split("\n")

                last_line: int = len(lines) - 1
                cnt: int = -1
                for line in lines:
                    if ++cnt == last_line:
                        tail_text = line
                    else:
                        yield line

            except Exception as exc:
                print(exc)


