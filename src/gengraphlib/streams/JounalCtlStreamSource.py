from typing import Self

import os
import asyncio as aio

from io import BufferedWriter

from ..proc.ProcLib import ProcBase
from ..streams.CmdStdoutStream import CmdStdoutStream
from ..proc.AppProcessBase import AppProcessBase
from ..graph.KeyValueSchema import KeyValueSchema
from ..graph.GraphMessages import IndexingProgressMsg
from ..bootlog.BootLogDir import BootLogDir

class JounalCtlStreamSource( ProcBase ):

    def __init__( self: Self,
            keyval_schema:   KeyValueSchema | None,
            progress: bool = False
        ) -> None:
        super( JounalCtlStreamSource, self ).__init__( "keyval-source" )
        self.keyval_schema:   KeyValueSchema  | None = keyval_schema
        self.cmd_stream:      CmdStdoutStream | None = None
        self.bootlogdir:      BootLogDir      | None = None
        self.bin_writer:      BufferedWriter  | None = None
        self.log_writer:      BufferedWriter  | None = None

        self.bin_filename: str | None = None
        self.log_filename: str | None = None
        self.progress:     bool = progress
        self.cnt:          int  = -1

    def launch_processing( self: Self, bootlogdir: BootLogDir, write_bin: bool, write_log: bool ) -> None:
        self.bootlogdir = bootlogdir
        self.cmd_stream = CmdStdoutStream(f"/bin/journalctl -b {self.bootlogdir.idx} -o export")
        
        if write_bin:
            self.bin_filename = os.path.join( self.bootlogdir.dir_path, "bootlog.bin" )
            self.bin_writer: BufferedWriter = open( self.bin_filename, "wb" )

        if write_log:
            self.log_writer = os.path.join( self.bootlogdir.dir_path, "bootlog.log" )
            self.log_writer: BufferedWriter = open( self.log_writer, "wb" )

        self.start()

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

    def recv_line( self: Self, line: bytes ) -> None:
        self.cnt += 1
        if self.bin_writer:
            self.bin_writer.write( line )
        if self.progress:
            self.print_progress()

        if len(line) > 0:
            split:       int   = line.find(b"=")
            keybuffer:   bytes = line[:split]
            valuebuffer: bytes = line[split+1:]

            log_key: str = keybuffer.decode()
            self.forward_keyvalue( log_key, valuebuffer )
        else:
            self.forward_keyvalue(None, None)

    def print_progress( self: Self ) -> None:
        if self.cnt % 100 == 0:
            print(".", end="")

        elif self.cnt % 1000 == 0:
            print(f"\ncnt: {self.cnt}")
            #msg = IndexingProgressMsg( source_id= "key-value-stream-proc", message = "Progress: ...", data = {"cnt": str( self.cnt )} )
            #AppProcessBase.instance.msg_queue.send_msg( msg )

        return None

    def forward_keyvalue( self: Self, log_key: str | None, valuebuffer: bytes | None ) -> None:
        if self.log_writer is not None:
            if log_key is not None and valuebuffer is not None:
                log_str = f"{log_key} : {valuebuffer}"
            else:
                log_str = "--------------- next record --------------- next record "

            self.log_writer.write(log_str.encode())



