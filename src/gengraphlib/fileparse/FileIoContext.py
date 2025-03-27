
from __future__ import annotations

from typing import TextIO, Self
from collections.abc import Callable

LINE_CALLBACK = Callable[ str, bool ]

class FileIoContext:

    def __init__( self: Self, input_file_name: str, output_file_name: str, line_fn: LINE_CALLBACK ) -> None:
        self.inputfn = input_file_name
        self.outputfn = output_file_name
        self.line_fn: Callable[str, bool] = line_fn

    def parse_file( self: Self ) -> None:
        reader: TextIO
        with open( self.input_file_name, newline = '', encoding = 'utf-8-sig' ) as reader:
            for line_str in reader:
                self.line_fn( line_str )
