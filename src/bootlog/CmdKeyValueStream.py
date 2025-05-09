from typing import Self

import asyncio as aio
import asyncio.subprocess as asub

from collections.abc import AsyncGenerator

from loguru import logger

from ..gengraphlib import KeyValueTuple

#from .LineSlicer import LineSlicer

class CmdKeyValueStream:

    def __init__(self: Self, cmd: str ) -> None:
        super().__init__()

        self.cmd:       str = cmd
        #self.tail_text: str = ""

        #self.line_slicer = LineSlicer()

    async def stream_values( self: Self ) -> AsyncGenerator[ KeyValueTuple, None ]:

        exec_process: asub.Process | None = None
        try:
            exec_process: asub.Process = \
                await aio.create_subprocess_shell(
                    cmd=self.cmd
                    #stdout=aio.subprocess.PIPE
                )

        except Exception as exc:
            logger.error(f"Exception {exc}")

        if exec_process is None:
            logger.error(f"create_subprocess_shell({self.cmd}) returned None")
        else:
            logger.info("stream started")
            while True:
                try:
                    stdout, stderr = await exec_process.communicate()
                    if stderr:
                        print(f"Error: {stderr.decode()}")

                    nullbuf = bytearray(1)
                    nullbuf[0] = 0

                    #buffer = stdout.replace( nullbuf, b'%' )

                    bufstr = stdout.decode('latin1')

                    for line in bufstr.split('\n'):
                        if len(line)==0:
                            yield '',''

                        first_equals: int = bufstr.find("=")
                        key:          str = bufstr[:first_equals]
                        value:        str = bufstr[first_equals:]
                        yield key, value
                        #logger.info( f'{key}  |  {value} )')

                except Exception as exc:
                    logger.error(f"Exception on {self.cmd}   {exc}")
                    break

            logger.info("stream finished")

