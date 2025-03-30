from abc import abstractmethod

from typing import Self
import asyncio as aio
import asyncio.subprocess as asub

from collections.abc import Coroutine
from typing import Any
from enum import IntEnum

comm_result_coroutine = Coroutine[Any, Any, tuple[bytes,bytes ] ]
comm_result_streams = tuple[bytes,bytes ]
comm_result = comm_result_coroutine | comm_result_streams

ExecResult: type = Coroutine[Any, Any, asub.Process ]
ReadResult: type = Coroutine[Any, Any, bytes ]

class CommResultKind(IntEnum):
    CoroutineAndStreams = 1
    StreamsOnly = 2

class PipedCmdBase:
    def __init__(self: Self, pipe_name: str  ) -> None:
        self.cmd: str | None = None
        self.name: str = pipe_name
        self.proc = None
        self.proc_ret_value: int | None = None
        self.proc_result: comm_result | None = None
        self.exec_process: asub.Process | None = None
        self.started: bool = False
        self.error: int = 0

    async def run_command(self: Self, cmd: str) -> bool:
        try:
            self.cmd = cmd
            self.exec_process: asub.Process = await aio.create_subprocess_exec(
                self.cmd,
                stdin=aio.subprocess.PIPE,
                stdout=aio.subprocess.PIPE,
                stderr=aio.subprocess.PIPE
            )
            if self.exec_process is None:
                self.error = -1
                return False
            else:
                if self.exec_process.returncode > 0:
                    self.error = self.exec_process.returncode
                    return False
                else:
                    self.proc_result = await self.exec_process.communicate()
                    self.started = True

                    await self._receive_lines()
                    return True

        except Exception as exc:
            print(f'SubprocessExec.run_command: {exc}')
            self.error = -2
            return False

    async def _receive_lines(self: Self ) -> bool:
        while True:
            try:
                line = await self.proc.stdout.readline()
                if line:
                    self.process_line( line.decode().strip() )
                else:
                    break

            except Exception as exc:
                print(f'SubprocessExec.run_command: {exc}')
                return False

        return True

    async def _forward_line( self, line: str ) -> bool:
        try:
            line = await self.proc.stdin.write(line.encode())
            if line:
                self.process_line( line.decode().strip() )

        except Exception as exc:
            print(f"SubprocessExec.run_command: {exc}")
            return False

        return True

    @abstractmethod
    def process_line( self: Self, line: str ) -> bool:
        return True

class PipedToFileBase(PipedCmdBase):

    def __init__( self: Self, pipe_name: str, output_filename: str ) -> None:
        self.output_filename = output_filename
        self.output_file = open( self.output_filename, "w" )
        super().__init__(pipe_name)

    async def process_line( self: Self, line: str ) -> bool:
        try:
            print(line)
            if self.output_file is not None:
                self.output_file.write(line)
                self.output_file.write("\n")
                self.output_file.flush()
            else:
                return True

        except Exception as exc:
            print(f'[PipedToFile: {self.name}] Exception: {exc}')
            self.started = False
            self.error = -3
            return False

        return True

class PipeToPipeBase(PipedCmdBase):

    def __init__( self: Self, pipe_name: str ) -> None:
        super().__init__(pipe_name)

    async def process_line( self: Self, line: str ) -> bool:
        try:
            print(line)

            return True

        except Exception as exc:
            print(f'[PipeToPipeBase:{self.name}] Exception: {exc}')
            self.started = False
            self.error = -3
            return False


