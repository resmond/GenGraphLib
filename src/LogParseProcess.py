import os
import subprocess
from typing import Self
import asyncio as aio
import multiprocessing as mp

from loguru import logger
from sortedcontainers import SortedSet, SortedDict

from src.bootlog import (
#    CmdKeyValueStream,
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

        logger.add(
            "/home/richard/data/jctl-logs/GenGraphLib.log",
            format="{time} {level} {message}",
            filter="gengraphlib",
            level="INFO"
        )

        parse_info: ParseProcessInfo = parse_info
        self.log_root: str           = parse_info.log_root
        self.cur_bootindex: int      = parse_info.boot_index
        self.app_msgqueue: mp.Queue  = parse_info.app_msgqueue

        self.log_manager: BootLogManager  = BootLogManager( self.log_root )
        self.cur_bootlog: BootLog  = self.log_manager.get_bootlog( boot_index = self.cur_bootindex )

        self.bootlog_path = self.cur_bootlog.get_bootlogpath()
        self.logfile = os.path.join(self.cur_bootlog.bootlog_path, 'bootrec.log' )

        self.table_model: LogEventModel   = LogEventModel()
        self.queues_byalias: dict[str, mp.Queue ] = self.table_model.init_import( self.app_msgqueue )

        self.cmd: str = f"/bin/journalctl -b {self.cur_bootindex} -o export > {self.logfile}"
        #self.cmd_stream:  CmdKeyValueStream = CmdKeyValueStream( self.cmd )
        self.record_count: int = 0

        self.local_stats: dict[str, StatsValCounter ] = dict[str, StatsValCounter ]()
        self.record_profiles: SortedDict[str, int] = SortedDict[str, int]()

    def update_stats( self: Self, keyvalue: str, value: str ):
        if keyvalue not in self.local_stats:
            self.local_stats[ keyvalue ] = StatsValCounter( value )
        else:
            self.local_stats[ keyvalue ].next_value( value )

    async def run_import( self: Self ) -> None:

        try:
            try:
                subprocess.run(
                    self.cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                )
            except subprocess.CalledProcessError as e:
                print(f"Error executing command: {e}")
                print(f"Error output: {e.stderr}")

            logger.info("log process done")

            alias_set: SortedSet[str] = SortedSet[str]()

            with open(self.logfile, buffering=1, encoding='latin1' ) as file:
                for line in file:

                    line = line.replace('\x00', '' )
                    first_equals = line.find("=")

                    if first_equals == -1:
                        continue

                    alias: str = line[:first_equals]
                    value: str = line[first_equals + 1 : -1]

                    if alias == "__CURSOR":
                        self.record_count += 1
                        continue

                        #profile_str: str = ' '.join(alias_set)
                        # alias_set = SortedSet[str]()
                        # if profile_str not in self.record_profiles:
                        #     self.record_profiles[profile_str] = 0
                        # self.record_profiles[profile_str] += 1

                        # if self.record_count % 100 == 0:
                        #     logger.info(f'record_count = {self.record_count}')


                    # if alias in alias_set:
                    #     logger.error(f"duplicate: {alias}")
                    # else:
                    #     alias_set.add(alias)
                    # self.update_stats(alias, value)

                    if alias in self.queues_byalias:
                        keyindex_queue: mp.Queue = self.queues_byalias[alias]
                        keyindex_queue.put( (self.record_count,value) )

            for alias, keyindex_queue in self.queues_byalias.items():
                value_packet: KeyValuePacket = (-1, str(self.record_count))
                keyindex_queue.put(value_packet)

        except Exception as exc:
            logger.error(f'Exception: {exc}')

    def parse_completed( self: Self ) -> None:
        self.table_model.wait_tocomplete()

        filepath: str = os.path.join( self.bootlog_path, "logevents.parquet" )
        self.table_model.save_table(filepath)
        #self.dump_stats( filepath )

    def dump_stats( self: Self, filepath: str ):
        with open(f'{filepath}.profiles','w') as file:
            for profile_str, cnt in self.record_profiles.items():
                file.write(f'found_cnt: {cnt:5}  {profile_str}\n')

        with open(f'{filepath}.noise',"w") as file:
            for profile_str, stats in self.local_stats.items():
                keycnt: int = len(stats.keymap)
                refcnt: int = 0
                for value, cnt in stats.keymap.items():
                    refcnt += cnt
                hitpct: int = round((refcnt / self.record_count) * 100)
                logger.info(f'{profile_str:30}: keycnt: {keycnt:6}  refcnt: {refcnt:6}  hitpct: {hitpct}')
                file.write(f'{profile_str:30}: keycnt: {keycnt:6}  refcnt: {refcnt:6}  hitpct: {hitpct}\n')




