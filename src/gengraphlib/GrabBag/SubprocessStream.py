from typing import Self

from collections.abc import AsyncGenerator
import asyncio as aio
import asyncio.subprocess as asub

class SubprocessStream:

    def __init__(self: Self):
        self.cmd: str | None = None
        self.exec_process: asub.Process | None = None
        self.started: bool = False
        self.error: int = 0
        self.exc: Exception | None = None

    async def run_command(self: Self, cmd: str, exec_dir: str) -> AsyncGenerator[ str, None ]:
        try:
            self.exec_process: asub.Process = await aio.create_subprocess_shell(
                cmd,
                cwd=exec_dir,
                stdout=aio.subprocess.PIPE,
            )

            while True:
                line = await self.exec_process.stdout.readline()
                if line:
                    yield line.decode().strip()
                else:
                    break

        except Exception as exc:
            print(f'SubprocessExec.run_command: {exc}')
            self.exc = exc
            self.error = -1


async def main():

    subprocess = SubprocessStream()
    async for line in subprocess.run_command("journalctl -b -1 -o json", "/home/richard/data/jctl-logs"):
        print(line)

if __name__ == "__main__":
    aio.run( main() )