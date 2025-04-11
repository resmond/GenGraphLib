from typing import Self

from collections.abc import AsyncGenerator
import asyncio as aio

from .CmdStreamBase import CmdStreamBase

class CmdStreamBinary(CmdStreamBase):

    def __init__(self: Self, cmd: str | None = None):
        super().__init__(cmd)


    async def stream_binary( self: Self, cmd: str | None = None, buffer_size: int = 16384 ) -> AsyncGenerator[ bytes, None ]:
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

async def main():

    with open("/home/richard/data/jctl-logs/boots/2024-12-08T17:44:02/logdata.bin", "wb") as fileout:
        subprocess = CmdStreamBinary()
        filelen: int = 0
        async for binary in subprocess.stream_binary("journalctl -b -1 -o json"):
            filelen += len(binary)
            print(f"[{len(binary)}]\n{binary}")
            fileout.write(binary)

    print(f"data written: {filelen} bytes")

if __name__ == "__main__":
    aio.run( main() )