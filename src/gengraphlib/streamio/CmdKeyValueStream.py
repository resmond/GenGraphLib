from typing import Self

from collections.abc import AsyncGenerator

import asyncio as aio
import asyncio.subprocess as asub

class CmdKeyValueStream:

    def __init__(self: Self, cmd: str ):
        self.cmd: str = cmd

    async def pipe( self: Self ) -> AsyncGenerator[ bytes, None ]:
        if self.cmd is None:
            print("CmdChainSource.pipe(): No command")
            return

        exec_process: asub.Process = await aio.create_subprocess_shell(
            cmd=self.cmd,
            stdout=aio.subprocess.PIPE
        )

        if exec_process is None:
            return

        while True:
            if read_buffer := await exec_process.stdout.read( self.buffer_size ):
                yield read_buffer

# async def test():
#     log_graph = BootLogGraph( id="1", _log_root = "/home/richard/data/jctl-logs/" )
#     start = time.time()
#     print(f"start: {start}")
#     with open("/home/richard/data/jctl-logs/rawout.bin", "wb") as writer:
#         command_source = CmdKeyValueStream( "journalctl -b -1 -o export", log_graph )
#         async for buffer_result in command_source.pipe():
#             if buffer_result is not None:
#                 writer.write( buffer_result )
#
#     end = time.time()
#     print(f"end: {end}")
#     print(f"elapsed: {end-start}")
#
#     if __name__ == "__main__":
#         aio.run( test() )
