from typing import Self

from collections.abc import AsyncGenerator
import asyncio as aio

from .CmdStreamBase import CmdStreamBase

class CmdStreamText(CmdStreamBase):

    def __init__(self: Self, cmd: str | None = None):
        super().__init__(cmd)

    async def stream_textlines( self: Self, cmd: str | None = None ) -> AsyncGenerator[ str, None ]:
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

async def main():

    with open("/home/richard/data/jctl-logs/boots/2024-12-08T17:44:02/logdata.txt", "w") as fileout:
        subprocess = CmdStreamText()
        filelen: int = 0
        async for line in subprocess.stream_textlines("journalctl -b -1 -o json"):
            filelen += len(line)
            fileout.writelines(line)

    print(f"data written: {filelen} bytes")

if __name__ == "__main__":
    aio.run( main() )