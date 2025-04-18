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
        self.writer:          BufferedWriter  | None = None

        self.out_filename: str | None = None
        self.out_filename: str | None = None
        self.progress:     bool = progress
        self.cnt:          int  = -1

    def launch_processing( self: Self, bootlogdir: BootLogDir, write_bin: bool ) -> None:
        self.bootlogdir = bootlogdir
        self.cmd_stream = CmdStdoutStream(f"jounalctl -b {self.bootlogdir.idx} -o export")
        
        if write_bin:
            filepath = os.path.join( self.bootlogdir.dir_path, f"bootlog-{self.bootlogdir.idx}.bin" )
            self.writer: BufferedWriter = open(filepath, "wb")

        self.start()

    def main_loop(self: Self) -> None:
        aio.run(self.spin_stream())

    async def spin_stream( self: Self ) -> None:
        async for line in self.cmd_stream.line_stream():
            self.recv_line(line)

    def recv_line( self: Self, line: bytes ) -> None:
        self.cnt += 1
        if self.writer:
            self.writer.write(line)
        if self.progress:
            self.print_progress()

        split:       int   = line.find(b"=")
        keybuffer:   bytes = line[:split]
        valuebuffer: bytes = line[split+1:]

        log_key: str = keybuffer.decode()

        self.forward_keyvalue( log_key, valuebuffer )

    def print_progress( self: Self ) -> None:
        if self.cnt % 100 == 0:
            print(".", end="")

        elif self.cnt % 1000 == 0:
            print(f"\ncnt: {self.cnt}")
            msg = IndexingProgressMsg( source_id= "key-value-stream-proc", message = "Progress: ...", data = {"cnt": str( self.cnt )} )
            AppProcessBase.instance.msg_queue.send_msg( msg )

        return None

    def forward_keyvalue( self: Self, log_key: str, valuebuffer: bytes ) -> None:
        pass


