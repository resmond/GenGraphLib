from typing import Self
from io import BufferedWriter

from src.gengraphlib.proc.ProcLib import ProcBase
from src.gengraphlib.streams.CmdStdoutStream import CmdStdoutStream
from src.gengraphlib.proc.AppProcessBase import AppProcessBase
from src.gengraphlib.graph.KeyValueSchema import KeyValueSchema
from src.gengraphlib.graph.GraphMessages import IndexingProgressMsg
from src.gengraphlib.bootlog.BootLogManager import BootLogManager
from src.gengraphlib.bootlog.BootLogDir import BootLogDir

class KeyValueStreamProc( ProcBase ):

    def __init__( self: Self,
            keyval_schema:   KeyValueSchema | None,
            bootlog_manager: BootLogManager | None = None,
            specific_ndx: int | None = None,
            out_filename: str | None = None,
            progress: bool = False
        ) -> None:
        super(KeyValueStreamProc, self).__init__("keyval-source")
        self.keyval_schema:   KeyValueSchema  | None = keyval_schema
        self.bootlog_manager: BootLogManager  | None = bootlog_manager
        self.cmd_stream:      CmdStdoutStream | None = None
        self.log_dir:         BootLogDir      | None = None
        self.writer:          BufferedWriter  | None = None

        self.out_filename: str  = out_filename
        self.specific_ndx: int  = specific_ndx
        self.progress:     bool = progress
        self.cnt:          int  = -1

        if bootlog_manager and specific_ndx:
            self.log_dir: BootLogDir = self.log_manager.get_bootlogdir(specific_ndx)
        if out_filename:
            self.writer: BufferedWriter = open(out_filename, "wb")

        self.cmd_stream = CmdStdoutStream(f"jounalctl -b {specific_ndx} -o export")

    def main_loop(self: Self) -> None:
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

        self.process_keyvalue(log_key, valuebuffer)

    def print_progress( self: Self ) -> None:
        if self.cnt % 100 == 0:
            print(".", end="")

        elif self.cnt % 1000 == 0:
            print(f"\ncnt: {self.cnt}")
            msg = IndexingProgressMsg( source_id= "key-value-stream-proc", message = "Progress: ...", data = {"cnt": str( self.cnt )} )
            AppProcessBase.instance.msg_queue.send_msg( msg )

        return None

    def process_keyvalue( self: Self, log_key: str, valuebuffer: bytes ) -> None:
        pass


