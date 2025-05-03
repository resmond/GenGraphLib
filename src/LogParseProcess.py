from typing import Self
import multiprocessing as mp

from .bootlog import (
    CmdStdoutStream,
    BootLogManager,
    BootLog
)

from gengraphlib import KeyValuePacket

from .LogEventModel import LogEventModel

class ParseProcessInfo:
    def __init__( self: Self, app_msgqueue: mp.Queue, end_event: mp.Event, id: str, log_root: str, boot_index: int ) -> None:
        super().__init__()

        self.app_msgqueue: mp.Queue = app_msgqueue
        self.end_event:    mp.Event = end_event
        self.id:           str      = id
        self.log_root:     str      = log_root
        self.boot_index:   int      = boot_index

class LogParseProcess:

    @staticmethod
    def entrypoint( parse_info: ParseProcessInfo ) -> None:

        parse_manager = LogParseProcess( parse_info )
        parse_manager.launch_indexing()

    def __init__( self: Self, parse_info: ParseProcessInfo | None = None ) -> None:
        super().__init__()

        self.cnt:           int  = 0

        parse_info: ParseProcessInfo | None = parse_info
        self.cur_bootindex: int  = parse_info.boot_index
        self.app_msgqueue: mp.Queue = parse_info.app_msgqueue
        self.end_event:    mp.Event = parse_info.end_event


        self.cmd: str = f"/bin/journalctl -b {self.bootlog_info.boot_index} -o export"
        self.cmd_stream:  CmdStdoutStream = CmdStdoutStream( self.cmd )


        self.table_model: LogEventModel   = LogEventModel()
        self.log_manager: BootLogManager  = BootLogManager( self.log_root )
        self.cur_bootlog: BootLog  = self.log_manager.get_bootlog( boot_index = self.cur_bootindex )
        self.queues_byalias: dict[str, mp.Queue ] | None = None


    def launch_indexing( self: Self ) -> None:
        self.queues_byalias = self.table_model.init_import( self.app_msgqueue )
        return None

    async def _parseloop( self: Self ) -> bool:

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







    



