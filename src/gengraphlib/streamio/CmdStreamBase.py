from typing import Self

import asyncio as aio
import asyncio.subprocess as asub

class CmdStreamBase:

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

