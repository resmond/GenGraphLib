from typing import Self

import asyncio as aio
import asyncio.subprocess as asub

from collections.abc import AsyncGenerator

from ..gengraphlib import KeyValueTuple

from .LineSlicer import LineSlicer

class CmdKeyValueStream:

    def __init__(self: Self, cmd: str ) -> None:
        super().__init__()

        self.cmd: str = cmd
        self.tail_text: str = ""

        self.line_slicer = LineSlicer()

    async def stream_values( self: Self ) -> AsyncGenerator[ KeyValueTuple, None ]:

        exec_process: asub.Process = await aio.create_subprocess_shell( cmd=self.cmd, stdout=aio.subprocess.PIPE, limit = 16*1024 )
        if exec_process is None:
            return

        print("CmdStdoutStream: stream started")
        line_cnt: int = -1
        while True:
            try:
                buffer = await exec_process.stdout.read(1024*256)

                if buffer is None or len(buffer) == 0:

                    keyvalue_tuple = self.line_slicer.get_tail()
                    if len(keyvalue_tuple) > 0:
                        yield keyvalue_tuple

                    break
                else:
                    for keyvalue_tuple in self.line_slicer.pass_buffer( buffer ):
                        line_cnt += 1
                        yield keyvalue_tuple

                    # new_text = buffer.decode(errors="replace")
                    # merged_text = self.tail_text + new_text
                    # lines: list[str] = merged_text.split("\n")
                    # if lines:
                    #     self.tail_text = lines.pop()
                    #
                    #     for line in lines:
                    #         #print(f'[{line_cnt}] {line}')
                    #         line_cnt += 1
                    #         yield line
                    # else:
                    #     print(f"CmdStdoutStream: {self.cmd} - lines empty" )

            except Exception as exc:
                #breakpoint()
                print(f"CmdStdoutStream: Exception on {self.cmd}")
                print(f"    {exc}")

        print("CmdStdoutStream: stream ended")




