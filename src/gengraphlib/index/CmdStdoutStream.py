from typing import Self

import os

import asyncio as aio
import asyncio.subprocess as asub
import multiprocessing as mp

from io import BufferedWriter
from collections.abc import AsyncGenerator

class CmdStdoutStream:

    def __init__(self: Self, cmd: str, end_event: mp.Event, write_bin: bool ):
        self.cmd: str = cmd
        self.write_bin: bool = write_bin
        self.bin_writer: BufferedWriter | None = None
        self.end_event: mp.Event = end_event
        self.tail_text: str = ""

    async def stream_lines( self: Self, ) -> AsyncGenerator[ str, None ]:
        if self.cmd is None:
            print("CmdStdoutStream: No command")
            return

        exec_process: asub.Process = await aio.create_subprocess_shell( cmd=self.cmd, stdout=aio.subprocess.PIPE, limit = 16*1024 )

        if exec_process is None:
            return

        print("CmdStdoutStream: stream started")

        if self.write_bin:
            self.bin_writer = open( os.path.join( self.bootlog_info.dir_path, "bootlog.bin" ), "wb" )

        while True:

            try:
                buffer = await exec_process.stdout.read(1024*16)
                if not self.end_event or buffer is None or len(buffer) == 0:
                    break
                else:
                    if self.write_bin:
                        self.bin_writer.write(buffer)

                    new_text = buffer.decode(errors="replace")
                    lines: list[str] = (self.tail_text + new_text).split("\n")
                    self.tail_text = lines.pop()

                    for line in lines:
                        yield line

            except Exception as exc:
                print(f'CmdStdoutStream: Exception on {self.cmd}')
                print(f'    {exc}')

        if self.bin_writer is not None:
            self.bin_writer.close()

        print("CmdStdoutStream: stream ended")




