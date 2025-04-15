from __future__ import annotations

from typing import Self

from collections.abc import AsyncGenerator, Callable

import asyncio as aio
import asyncio.subprocess as asub

from .. import GraphRecordRoot

dispatch_fn: Callable[str, None] | None = None

class KeyValueDispatcher(dict[bytes,dispatch_fn]):

    def __init__(self: Self, key_schema: GraphRecordRoot ):
        super(KeyValueDispatcher, self).__init__()
        self.key_schema: GraphRecordRoot = key_schema

class CmdKeyValueStream:

    def __init__(self: Self, cmd: str, key_schema: GraphRecordRoot ):
        self.key_schema: GraphRecordRoot = key_schema
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
