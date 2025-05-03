import os
from io import BufferedWriter
from typing import Self

import multiprocessing as mp
import asyncio as aio
import time

from src.gengraphlib.common import KeyType, KeyValSchemaInfo, KeyValuePacket, IndexTaskInterface, BootLogInfo

from src.gengraphlib.graphs import GraphTable

from src.gengraphlib.index.CmdStdoutStream import CmdStdoutStream

from src.gengraphlib.index.StrIndexingTask import StrIndexingTask
from src.gengraphlib.index.IntIndexingTask import IntIndexingTask
from src.gengraphlib.index.BoolIndexingTask import BoolIndexingTask
from src.gengraphlib.index.FloatIndexingTask import FloatIndexingTask
from src.gengraphlib.index.TmstIndexingTask import TmstIndexingTask


# noinspection PyUnresolvedReferences
class LogIndexingProcess:

    def __init__(
        self: Self,
        schema_info: KeyValSchemaInfo,
        app_msgqueue: mp.Queue,
        end_event: mp.Event
    ) -> None:
        super().__init__()

        self.schema_info:  KeyValSchemaInfo = schema_info
        self.app_msgqueue: mp.Queue         = app_msgqueue
        self.end_event:    mp.Event         = end_event

        self.queues_byalias: dict[str, mp.Queue ] = dict[str, mp.Queue ]()
        self.indextask_map:  dict[str, IndexTaskInterface ] = dict[str, IndexTaskInterface ]()

        self.cmd_stream: CmdStdoutStream | None = None
        self.log_writer: BufferedWriter  | None = None

        self.bootlog_info: BootLogInfo | None = None
        self.graph_table:  GraphTable  | None = None
        self.active_keys:  set[str] | None = None
        self.state:        str = "Init"
        self.write_bin:    bool = False
        self.write_log:    bool = False
        self.record_count: int = 0

    def index_bootlog(
        self: Self,
        bootlog_info: BootLogInfo,
        graph_table: GraphTable,
        active_keys: set[str],
        write_bin: bool = False,
        write_log: bool = False,
    ) -> None:

        self.bootlog_info = bootlog_info
        self.graph_table  = graph_table
        self.active_keys  = active_keys
        self.write_bin    = write_bin
        self.write_log    = write_log

        if write_log:
            self._start_logwriter()

        self._start_indexes()
        self.state = "indexes-started"

        time.sleep(.1)
        print("starting stream")
        aio.run( self._stream_exec() )

    def _start_logwriter( self ) -> None:
        log_filepath = os.path.join(self.bootlog_info.dir_path, "bootlog.log")
        try:
            self.log_writer: BufferedWriter = open(log_filepath, "wb")
        except Exception as logext:
            print(f"ValueIndexMsgPump: open( {log_filepath} ) Exception - {logext}")
            self.write_log = False

    def _register_indextask(self: Self, index: IndexTaskInterface) -> None:
        self.queues_byalias[ index.alias ] = index.queue
        self.indextask_map[  index.id()  ] = index
        index.start()

    def _start_indexes( self: Self ) -> None:
        for keyinfo in self.schema_info.keys:
            if keyinfo.alias in self.active_keys:
                match keyinfo.keytype:
                    case KeyType.KStr:
                        self._register_indextask( StrIndexingTask( keyinfo, self.bootlog_info, self.graph_table, self.app_msgqueue, self.end_event ) )
                    case KeyType.KInt:
                        self._register_indextask( IntIndexingTask( keyinfo, self.bootlog_info, self.graph_table, self.app_msgqueue, self.end_event ) )
                    case KeyType.KBool:
                        self._register_indextask( BoolIndexingTask( keyinfo, self.bootlog_info, self.graph_table, self.app_msgqueue, self.end_event ) )
                    case KeyType.KFloat:
                        self._register_indextask( FloatIndexingTask( keyinfo, self.bootlog_info, self.graph_table, self.app_msgqueue, self.end_event ) )
                    case KeyType.KTmst:
                        self._register_indextask( TmstIndexingTask( keyinfo, self.bootlog_info, self.graph_table, self.app_msgqueue, self.end_event ) )

    def stop_indexes(self: Self) -> None:
        for index in self.indextask_map.values():
            index.stop()

    async def _stream_exec( self: Self ) -> None:

        try:
            self.cmd: str = f"/bin/journalctl -b {self.bootlog_info.boot_index} -o export"
            self.cmd_stream = CmdStdoutStream(self.cmd, self.end_event, self.write_bin )

            await self._stream_innerloop()

        except Exception as exc:
            print(f'ValueIndexMsgPump: CmdStdoutStream( {self.cmd} ) Exception - {exc}  ')

        finally:
            if self.log_writer is not None:
                self.log_writer.close()

    async def _stream_innerloop( self: Self ) -> bool:

        try:
            async for line in self.cmd_stream.stream_lines():

                match line:
                    case str() if len(line) == 0:
                        self.record_count += 1

                        if self.write_log:
                            self.log_writer.write(f'next record: [{self.record_count}]  ---------------------------\n'.encode())

                    case _:

                        split: int = line.find("=")
                        alias: str = line[:split]
                        value: str = line[split + 1 :]

                        if alias in self.queues_byalias:
                            keyindex_queue: mp.Queue = self.queues_byalias[alias]
                            value_packet: KeyValuePacket = (self.record_count, value)
                            keyindex_queue.put(value_packet)

                            if self.write_log:
                                self.log_writer.write(
                                    f"sending to {alias}:( {self.record_count}, {value} )\n".encode()
                                )
                        # else:
                        #     if self.write_log:
                        #         self.log_writer.write( f"skipping {alias}: {value}\n".encode() )

            for alias, keyindex_queue in self.queues_byalias.items():
                value_packet: KeyValuePacket = (-1, str(self.record_count))
                keyindex_queue.put(value_packet)

            return True

        except Exception as exc:
            print(f'Exception: {exc}')
            return False
