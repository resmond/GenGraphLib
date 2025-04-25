from typing import Self

import os
import asyncio as aio
import multiprocessing as mp

from io import BufferedWriter

from ..common import KeyValuePacket
from ..streams.CmdStdoutStream import CmdStdoutStream
from ..bootlog.BootLogInfo import BootLogInfo

class ValueIndexMsgPump:

    def __init__( self: Self, bootlog_info: BootLogInfo, write_bin: bool, write_log: bool ) -> None:
        self.bootlog_info: BootLogInfo = bootlog_info
        self.boot_index: int = bootlog_info.boot_index
        self.cmd:        str = f"/bin/journalctl -b {self.boot_index} -o export"
        self.write_bin:  bool = write_bin
        self.write_log:  bool = write_log

        self.cmd_stream: CmdStdoutStream | None = None
        self.log_writer: BufferedWriter  | None = None

        if self.write_log:
            log_filepath = os.path.join( self.bootlog_info.dir_path, "bootlog.log" )
            try:
                self.log_writer: BufferedWriter = open( log_filepath, "wb" )
            except Exception as logext:
                print(f'ValueIndexMsgPump: open( {log_filepath} ) Exception - {logext}')
                self.write_log = False

        self.record_count: int  = 0

    def start_stream( self: Self, queues_byalias: dict[str, mp.Queue ], end_event: mp.Event ) -> None:
        aio.run( self.stream_exec( queues_byalias, end_event ) )

    async def stream_exec( self: Self, queues_byalias: dict[str, mp.Queue ], end_event: mp.Event ) -> None:

        try:
            self.cmd_stream = CmdStdoutStream(self.cmd, end_event, self.write_bin )

            await self._stream_innerloop( queues_byalias )

        except Exception as exc:
            print(f'ValueIndexMsgPump: CmdStdoutStream( {self.cmd} ) Exception - {exc}  ')

        finally:
            if self.log_writer is not None:
                self.log_writer.close()

    async def _stream_innerloop( self: Self, queues_byalias: dict[str, mp.Queue ] ) -> bool:

        try:
            async for line in self.cmd_stream.stream_lines():

                match line:
                    case None:
                        return True

                    case str() if len(line) == 0:
                        self.record_count += 1

                        if self.write_log:
                            self.log_writer.write(f'next record: [{self.record_count}]  ---------------------------'.encode())

                    case _:

                        if len(line) < 3:
                            print()

                        split: int = line.find("=")
                        alias: str = line[:split]
                        value: str = line[split + 1 :]

                        if alias in self.queues_byalias:
                            keyindex_queue: mp.Queue = queues_byalias[alias]
                            value_packet: KeyValuePacket = (self.record_count, value)
                            keyindex_queue.put(value_packet)

                            if self.write_log:
                                self.log_writer.write(
                                    f"sending to {alias}:( {self.record_count}, {value} )".encode()
                                )
                        else:
                            if self.write_log:
                                self.log_writer.write( f"skipping {alias}: {value}".encode() )

            return True

        except Exception as exc:
            print(f'Exception: {exc}')
            return False



