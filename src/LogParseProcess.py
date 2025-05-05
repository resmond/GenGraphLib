import os
from typing import Self
import asyncio as aio
import multiprocessing as mp

from src.bootlog import (
    CmdStdoutStream,
    BootLogManager,
    BootLog
)

from gengraphlib import KeyValuePacket

from src.LogEventModel import LogEventModel

#from gengraphlib.arrow import ArrowResults
#from gengraphlib.model import StatsModProp

class StatsValCounter:
    def __init__( self: Self, value: str ) -> None:
        self.keymap: dict[str,int] = { value: 1 }

    def next_value( self: Self, value: str ) -> None:
        if value not in self.keymap:
            self.keymap[value] = 1
        else:
            self.keymap[value] += 1
        return


class ParseProcessInfo:
    def __init__( self: Self, app_msgqueue: mp.Queue, log_root: str, boot_index: int ) -> None:
        super().__init__()

        self.app_msgqueue: mp.Queue = app_msgqueue
        self.log_root:     str      = log_root
        self.boot_index:   int      = boot_index

class LogParseProcess:

    @staticmethod
    def entrypoint( parse_info: ParseProcessInfo ) -> None:

        parse_manager = LogParseProcess( parse_info )
        aio.run(parse_manager.run_import())

        parse_manager.parse_completed()

    def __init__( self: Self, parse_info: ParseProcessInfo ) -> None:
        super().__init__()


        parse_info: ParseProcessInfo = parse_info
        self.log_root: str           = parse_info.log_root
        self.cur_bootindex: int      = parse_info.boot_index
        self.app_msgqueue: mp.Queue  = parse_info.app_msgqueue

        self.log_manager: BootLogManager  = BootLogManager( self.log_root )
        self.cur_bootlog: BootLog  = self.log_manager.get_bootlog( boot_index = self.cur_bootindex )
        self.bootlog_path = self.cur_bootlog.bootlog_path

        self.table_model: LogEventModel   = LogEventModel()
        self.queues_byalias: dict[str, mp.Queue ] = self.table_model.init_import( self.app_msgqueue )

        self.cmd: str = f"/bin/journalctl -b {self.cur_bootindex} -o export"
        self.cmd_stream:  CmdStdoutStream = CmdStdoutStream( self.cmd )
        self.record_count: int = 0

        self.local_stats: dict[str, StatsValCounter ] = dict[str, StatsValCounter ]()

    def update_stats( self: Self, keyvalue: str, value: str ):
        if keyvalue not in self.local_stats:
            self.local_stats[ keyvalue ] = StatsValCounter( value )
        else:
            self.local_stats[ keyvalue ].next_value( value )

    async def run_import( self: Self ) -> None:

        try:
            async for line in self.cmd_stream.stream_lines():

                scratchcnt: int = 0
                match line:
                    case str() if len(line) == 0:
                        self.record_count += 1

                    case _:

                        split: int = line.find("=")
                        alias: str = line[:split]
                        value: str = line[split + 1 :]

                        self.update_stats( alias, value )

                        if alias in self.queues_byalias:
                            keyindex_queue: mp.Queue = self.queues_byalias[alias]
                            value_packet: KeyValuePacket = (self.record_count, value)
                            keyindex_queue.put(value_packet)
                        else:
                            scratchcnt += 1
                            #print( f'starting {alias} scratchcnt: {scratchcnt}')
                            # statsprop = StatsModProp( name=alias, alias=alias )
                            # prop_msgqueue = statsprop.start_import( self.app_msgqueue )
                            # self.queues_byalias[ alias ] = prop_msgqueue
                            # await aio.sleep(0.1)
                            # value_packet: KeyValuePacket = (self.record_count, value)
                            # prop_msgqueue.put(value_packet)


            for alias, keyindex_queue in self.queues_byalias.items():
                value_packet: KeyValuePacket = (-1, str(self.record_count))
                keyindex_queue.put(value_packet)

        except Exception as exc:
            breakpoint()
            print(f'Exception: {exc}')


    def parse_completed( self: Self ) -> None:
        self.table_model.wait_tocomplete()

        filepath: str = os.path.join( self.bootlog_path, "logevents.parquet" )
        self.table_model.save_table(filepath)
        self.dump_stats( filepath )

    def dump_stats( self: Self, filepath: str ):
        with open(f'{filepath}.noise',"w") as file:
            for propname, stats in self.local_stats.items():
                keycnt: int = len(stats.keymap)
                refcnt: int = 0
                for value, cnt in stats.keymap.items():
                    refcnt += cnt
                hitpct = (refcnt / self.record_count) * 100
                print(f'{propname}: keycnt: {keycnt}  refcnt: {refcnt}  hitpct: {hitpct}\n')
                file.write(f'{propname}: keycnt: {keycnt}  refcnt: {refcnt}  hitpct: {hitpct}\n')




