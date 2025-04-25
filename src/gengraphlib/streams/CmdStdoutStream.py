from typing import Self

from collections.abc import AsyncGenerator
import multiprocessing as mp

import asyncio as aio
import asyncio.subprocess as asub

class CmdStdoutStream:

    def __init__(self: Self, cmd: str, end_event: mp.Event ):
        self.cmd: str = cmd
        self.end_event: mp.Event = end_event
        self.tail_text: str = ""

    async def line_stream( self: Self ) -> AsyncGenerator[ str, None ]:
        if self.cmd is None:
            print("CmdStdoutStream: No command")
            return

        exec_process: asub.Process = await aio.create_subprocess_shell( cmd=self.cmd, stdout=aio.subprocess.PIPE, limit = 16*1024 )

        if exec_process is None:
            return

        print("CmdStdoutStream: stream started")

        while not self.end_event:

            try:
                buffer = await exec_process.stdout.read(1024*16)
                if not buffer  or len(buffer) == 0:
                    break

                new_text = buffer.decode(errors="replace")
                lines: list[str] = (self.tail_text + new_text).split("\n")
                self.tail_text = lines.pop()

                for line in lines:
                    yield line

            except Exception as exc:
                print(f'CmdStdoutStream: Exception on {self.cmd}')
                print(f'    {exc}')

        print("CmdStdoutStream: stream ended")




