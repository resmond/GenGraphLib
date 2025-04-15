import time
from typing import Self

from collections.abc import AsyncGenerator

import asyncio as aio
import asyncio.subprocess as asub

from ChainableLib import ChainableResult, StreamType, ChainSourceBase


class BootLogChainResult( ChainableResult ):
    def __init__( self: Self, buf: bytes | None = None ) -> None:
        super(BootLogChainResult, self).__init__(buf)

class CmdChainSource(ChainSourceBase[BootLogChainResult]):

    def __init__(self: Self, cmd: str, stream_type: StreamType = StreamType.LfTextLine, buffer_size: int = 4096  ):
        super( CmdChainSource, self ).__init__(stream_type, buffer_size) #stream_type, buffer_size)
        self.newline_char: bytes = b'\n'
        self.cmd: str = cmd

        # match stream_type:
        #     case StreamType.LfTextLine:
        #         self.nlbk_memview = memoryview( b'\n' )
        #     case StreamType.CrLfTextLine:
        #         self.nlbk_memview = memoryview( b'\r\n' )

        #self.exec_process: asub.Process | None = None

    async def pipe( self: Self ) -> AsyncGenerator[ BootLogChainResult, None ]:
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
                yield BootLogChainResult(read_buffer)

async def test():
    start = time.time()
    print(f"start: {start}")
    with open("/home/richard/data/jctl-logs/rawout.bin", "wb") as writer:
        command_source = CmdChainSource( "journalctl -b -1 -o export" )
        chain_result: BootLogChainResult
        async for chain_result in command_source.pipe():
            if chain_result is not None:
                buffer = chain_result.dequeue()
                print(f"buffer: [{buffer}]")
                writer.write( buffer )
    end = time.time()
    print(f"end: {end}")
    print(f"elapsed: {end-start}")

if __name__ == "__main__":
    aio.run( test() )


