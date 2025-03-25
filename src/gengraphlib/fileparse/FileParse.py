
from __future__ import annotations

from typing import TextIO, Self
from collections.abc import Callable

class FileParseContext:

    def __init__( self: Self, input_file_name: str, output_file_name: str, line_fn: Callable[ str, bool] ) -> None:
        self.inputfn = input_file_name
        self.outputfn = output_file_name
        self.line_fn: Callable[str, bool] = line_fn
        self.reader: TextIO   = open( input_file_name, newline = '', encoding = 'utf-8-sig' )
        self.writer: TextIO = open( output_file_name, 'w', encoding='utf-8-sig' )

    def parse_file( self: Self ) -> None:

        for lineStr in self.reader:
            self.line_fn( lineStr )

    def write( self: Self, text_data: str ) -> None:
        self.writer.write(text_data)

    def close( self ) -> None:
        self.writer.close()
        self.reader.close()
