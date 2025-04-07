from typing import Self

from collections.abc import AsyncGenerator
import asyncio as aio
import asyncio.subprocess as asub

class CmdStreamBase:

    def __init__(self: Self, cmd: str | None = None, exec_dir: str | None = None):
        self.cmd: str = cmd
        self.exec_dir: str = exec_dir
        self.exec_process: asub.Process | None = None
        self.started: bool = False
        self.error: int = 0
        self.exc: Exception | None = None

    async def run_command(self: Self, cmd: str | None = None, exec_dir: str | None = None) -> AsyncGenerator[ str, None ]:

        if cmd is not None:
            self.cmd = cmd

        if exec_dir is not None:
            self.exec_dir = exec_dir

        if self.cmd is not None:
            try:
                self.started = True
                self.exec_process: asub.Process = \
                    await aio.create_subprocess_shell(
                        cmd=cmd,
                        cwd=exec_dir,
                        stdout=aio.subprocess.PIPE,
                    )

                while True:
                    try:
                        line = await self.exec_process.stdout.readline()

                    except aio.exceptions.TimeoutError as aioerr:
                        print(f'[BootLogDirBase.stream] Exception: {aioerr}')
                        self.started = False
                        self.exc = aioerr
                        self.error = -3
                        break

                    else:
                        if line:
                            try:
                                yield line.decode().strip()

                            except Exception as decode_err:
                                print(f'[BootLogDirBase.stream] Exception: {decode_err}')
                                self.started = False
                                self.exc = decode_err
                                self.error = -2
                        else:
                            break

            except Exception as exc:
                print(f"CmdStreamBase.run_command: {exc}")
                self.exc = exc
                self.started = False
                self.error = -1

        else:
            print('CmdStreamBase.run_command: No command')
            self.started = False
            self.error = -2


async def main():

    subprocess = CmdStreamBase()
    async for line in subprocess.run_command("journalctl -b -1 -o json", "/home/richard/data/jctl-bootlog"):
        print(line)

if __name__ == "__main__":
    aio.run( main() )