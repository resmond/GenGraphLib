from collections.abc import AsyncGenerator
from typing import Self

import asyncio as aio
import asyncio.subprocess as asub

class CmdStreamSource:

    def __init__(self: Self, cmd: str | None = None):
        super().__init__()
        self.cmd: str = cmd
        self.exec_process: asub.Process | None = None
        self.started: bool = False
        self.error: int = 0
        self.exc: Exception | None = None

    async def _run_command( self: Self, cmd: str | None = None ) -> bool:
        if cmd is not None:
            self.cmd = cmd

        if self.cmd is not None:

            try:
                self.started = True
                self.exec_process: asub.Process = await aio.create_subprocess_shell(
                    cmd=cmd,
                    stdout=aio.subprocess.PIPE,
                )

                return self.exec_process is not None

            except Exception as exc:
                print(f"CmdStreamBase.run_command: {exc}")
                self.exc = exc
                self.started = False
                self.error = -1

        else:
            print("CmdStreamBase.run_command: No command")
            self.started = False
            self.error = -2

        return False

    async def stream_binary( self: Self, cmd: str | None = None, buffer_size: int = 4096 ) -> AsyncGenerator[ bytes, None ]:

        self.started = True
        while self.started:
            try:
                self.started =  await self._run_command(cmd)

                if self.started and self.exec_process is not None:

                    try:

                        buffer = await self.exec_process.stdout.read( buffer_size )

                        if len(buffer) > 0:
                            #line_str = buffer.decode().strip()
                            yield buffer
                        else:
                            self.started = False
                            self.error = 0
                            break

                    except Exception as innerexc:
                        print(f"CmdStreamBinary.stream_binary: {innerexc}")
                        self.exc = innerexc
                        self.started = False
                        self.error = -1
                        break
                else:
                    self.error = -1
                    self.started = False

            except Exception as exc:
                print(f"CmdStreamBinary.stream_binary: {exc}")
                self.exc = exc
                self.started = False
                self.error = -1
                break

    async def stream_text( self: Self, cmd: str | None = None ) -> AsyncGenerator[ str, None ]:
        while True:
            try:
                if await self._run_command(cmd):
                    line = await self.exec_process.stdout.readline()
                    if len(line) > 0:
                        line_str = line.decode().strip()
                        #print(line_str)
                        yield line_str
                    else:
                        break

            except Exception as exc:
                print(f"CmdStreamText.stream_textlines: {exc}")
                self.exc = exc
                self.started = False
                self.error = -1
                break

