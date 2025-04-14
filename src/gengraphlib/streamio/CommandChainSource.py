from typing import Self

from collections.abc import AsyncGenerator

import asyncio as aio
import asyncio.subprocess as asub

from . import ChainSourceBase, ChainableResult, StreamType

class CommandChainSource[ T: ChainableResult ]( ChainSourceBase ):

    def __init__(self: Self, cmd: str, stream_type: StreamType = StreamType.LfTextLine, buffer_size: int = 4096  ):
        super( CommandChainSource, self ).__init__(stream_type, buffer_size)
        self.newline_char: bytes = b'\n'
        self.cmd: str = cmd

        # match stream_type:
        #     case StreamType.LfTextLine:
        #         self.nlbk_memview = memoryview( b'\n' )
        #     case StreamType.CrLfTextLine:
        #         self.nlbk_memview = memoryview( b'\r\n' )

        #self.exec_process: asub.Process | None = None

    async def _result_pipe( self: Self ) -> AsyncGenerator[T, None] | None:
        if self.cmd is not None:

            try:

                exec_process: asub.Process = await aio.create_subprocess_shell(
                    cmd=self.cmd,
                    stdout=aio.subprocess.PIPE,
                )

                if exec_process is not None:
                    chain_result: T = ChainableResult()
                    while True:
                        try:

                            read_buffer = await self.exec_process.stdout.read( self.buffer_size )
                            len_read: int = len(read_buffer)

                            if read_buffer is None or len_read == 0:
                                yield chain_result

                            stream_cursor.extend(read_buffer)
                            first_newline = stream_cursor.find(self.newline_char)

                            if first_newline == -1:
                                continue

                            chain_result.add_buffer( stream_cursor[0:first_newline] )


                            stream_cursor = stream_cursor[first_newline+1:]

                        except Exception as innerexc:
                            print(f"CmdStreamBinary.stream_binary: {innerexc}")


            except Exception as exc:
                print(f"CmdStreamBase.run_command: {exc}")

        else:
            print("CmdStreamBase.run_command: No command")




