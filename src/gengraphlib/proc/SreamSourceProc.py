import time
from typing import Self

import multiprocessing as mp

from ..graph import KeyValueSchema
from ..streamio.CmdKeyValueStream import CmdKeyValueStream
from ..proc.ProcLib  import ProcBase
from ..bootlog import BootLogManager, BootLogDir

class StreamSourceProc(ProcBase):

    def __init__(self: Self, keyval_schema: KeyValueSchema, bootlog_manager: BootLogManager, queue_size: int | None = None ) -> None:
        super(StreamSourceProc, self).__init__("journal_source", queue_size)
        self.keyval_schema = keyval_schema
        self.bootlog_manager = bootlog_manager
        self.cnt: int = 0
        self.process = mp.Process(target=self.exec, args=(-1,))

    def start( self: Self ) -> None:
        self.process.start()

    def main_loop(self: Self) -> None:
        pass

    async def exec(self: Self, specific_ndx: int):
        log_dir: BootLogDir = self.log_manager.get_bootlogdir(specific_ndx)

        start = time.time()
        print(f"start: {start}")

        with open("/home/richard/data/jctl-logs/rawout.bin", "wb") as writer:
            command_source = CmdKeyValueStream("journalctl -b -1 -o export")
            self.cnt = 0
            async for line in command_source.line_stream():
                writer.write(line)
                if len(line):
                    print("next record")
                    continue

                split: int = line.find(b"=")
                self.cnt += 1
                if self.cnt % 10 == 0:
                    print(".", end="")
                elif self.cnt % 100 == 0:
                    print(f"\ncnt: {self.cnt}")
                elif self.cnt % 1000 == 0:
                    print(f"\ncnt: {self.cnt}")
                    break

        end = time.time()
        print(f"end: {end}")
        print(f"elapsed: {end - start}")

        print(f"BootLogGraph.exec(): {self.id} LogDir: {log_dir.dir_path}")
