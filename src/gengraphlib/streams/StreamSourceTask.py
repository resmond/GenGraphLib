from typing import Self

import os
import asyncio as aio
import multiprocessing as mp

from io import BufferedWriter

from ..common import KeyRecordList, KeyRecordPacket
from ..proc.TaskLib import TaskBase
from ..streams.CmdStdoutStream import CmdStdoutStream
from ..bootlog.BootLogDir import BootLogDir

class StreamSourceTask( TaskBase ):

    def __init__(
        self: Self,
        bootlogdir: BootLogDir,
        active_keys: set[str],
        record_queue: mp.Queue,
    ) -> None:
        super( StreamSourceTask, self ).__init__( "keyval-source" )
        self.bootlogdir = bootlogdir
        self.active_keys:     set[str]   = active_keys

        self.record_queue:    mp.Queue = record_queue

        self.cmd_stream:      CmdStdoutStream | None = None
        self.bootlogdir:      BootLogDir      | None = None
        self.bin_writer:      BufferedWriter  | None = None
        self.log_writer:      BufferedWriter  | None = None

        self.record_list: KeyRecordList = []

        self.bin_filename: str | None = None
        self.log_filename: str | None = None

        self.cnt: int  = -1

    def launch_processing( self: Self, write_bin: bool, write_log: bool ) -> None:
        self.cmd_stream = CmdStdoutStream(f"/bin/journalctl -b {self.bootlogdir.id} -o export" )
        
        if write_bin:
            self.bin_filename = os.path.join( self.bootlogdir.dir_path, "bootlog.bin" )
            self.bin_writer: BufferedWriter = open( self.bin_filename, "wb" )

        if write_log:
            self.log_filename = os.path.join( self.bootlogdir.dir_path, "bootlog.log" )
            self.log_writer: BufferedWriter = open( self.log_filename, "wb" )

        self.main_loop()

    def stop(self: Self) -> None:
        if self.log_writer is not None:
            self.log_writer.close()

        if self.bin_writer is not None:
            self.bin_writer.close()

    def main_loop(self: Self) -> None:
        aio.run(self.spin_stream())

    async def spin_stream( self: Self ) -> None:
        async for line in self.cmd_stream.line_stream():
            self.recv_line(line)

    def recv_line( self: Self, buffer: bytes ) -> None:
        self.cnt += 1

        line: str = buffer.decode()

        if self.bin_writer:
            self.bin_writer.write( buffer )
            
        # if self.progress:
        #     self.send_progress()

        if len(line) > 0:
            split:       int = line.find("=")
            key:   str = line[:split]
            value: str = line[split+1:]

            if key in self.active_keys:
                self.record_list.append( (key, value) )
        else:

            keyrecord_packet: KeyRecordPacket = ( self.cnt, self.record_list )
            self.record_queue.put( keyrecord_packet )
            self.record_list = []

    def send_progress( self: Self ) -> None:
        if self.cnt % 100 == 0:
            print(".", end="")

        elif self.cnt % 1000 == 0:
            print(f"\ncnt: {self.cnt}")
            #msg = IndexingProgressMsg( source_id= "key-value-stream-proc", message = "Progress: ...", data = {"cnt": str( self.cnt )} )
            #AppProcessBase.instance.msg_queue.send_msg( msg )

        return None

    def log_keyvalue( self: Self, log_key: str | None, valuebuffer: str | None ) -> None:
        if self.log_writer is not None:
            if log_key is not None and valuebuffer is not None and log_key in self.active_keys:
                log_str = f"{log_key}={valuebuffer}"
            else:
                log_str = "--------------- next record --------------- next record "
            self.log_writer.write(log_str.encode())



