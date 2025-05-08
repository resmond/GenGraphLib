from typing import Self

import asyncio as aio
import asyncio.subprocess as asub

from collections.abc import AsyncGenerator

from loguru import logger

from ..gengraphlib import KeyValueTuple

from .LineSlicer import LineSlicer

class CmdKeyValueStream:

    def __init__(self: Self, cmd: str ) -> None:
        super().__init__()

        self.cmd:       str = cmd
        self.tail_text: str = ""

        self.line_slicer = LineSlicer()

    async def stream_values( self: Self ) -> AsyncGenerator[ KeyValueTuple, None ]:

        exec_process: asub.Process | None = None
        try:
            exec_process: asub.Process = await aio.create_subprocess_shell( cmd=self.cmd, stdout=aio.subprocess.PIPE )

        except Exception as exc:
            logger.error(f"Exception {exc}")

        if exec_process is None:
            logger.error(f"create_subprocess_shell({self.cmd}) returned None")
        else:
            logger.info("stream started")
            while True:
                try:
                    buffer = await exec_process.stdout.read(1024*256)

                    if buffer is None or len(buffer) == 0:
                        logger.info("Buffer reached empty")

                        keyvalue_tuple = self.line_slicer.get_tail()
                        if keyvalue_tuple:
                            yield keyvalue_tuple
                            
                        break
                    else:
                        for keyvalue_tuple in self.line_slicer.pass_buffer( buffer ):
                            yield keyvalue_tuple

                except Exception as exc:
                    logger.error(f"Exception on {self.cmd}   {exc}")
                    break

            logger.info("stream finished")

