from __future__ import annotations

from abc import abstractmethod
from collections.abc import Iterable
from enum import IntEnum
#from importlib.metadata import always_iterable
from typing import Self, TextIO
import collections.abc as abc

from numpy.f2py.auxfuncs import throw_error

from progress.bar import Bar

class ParseState( IntEnum ):
    Working      =  0
    UnknownErr   = -1
    OpenErr      = -2
    StdException = -3


#LineRef = NamedTuple("LineRef", [ ("file_id", int),("line_num", int), ("line", str) ] )

def test_print( line_ref: LineRef ) -> bool:
    file_id = line_ref.file_id
    line_num = line_ref.line_num
    line = line_ref.line
    print(f'[test_print: ({file_id}:{line_num})]  {line}' )
    return True

class LineRef:

    def __init__(self):
        self.file_id: int | None = None
        self.line_num: int | None = None
        self.line: str | None = None

class ParseContextBase( Iterable[LineRef]  ):

    def __iter__( self ):
        pass

    def __init__(self: Self) -> None:
        self.state: ParseState = ParseState.Working
        self.pipe_name: str | None = None
        self.last_exception: Exception | None = None
        self.message: str | None = None
        self.upstream: ParseContextBase | None = None
        self.downstream: ParseContextBase | None = None
        self.pipe_id: int | None = None

    def __bool__(self) -> bool:
        return self.state != ParseState.Working

    async def pull_fileref( self ) -> Self:
        if self.upstream:
            return await self.upstream.pull_fileref()
        else:
            throw_error("No upstream context available")

    async def accept_fileref( self, fileref: LineRef ) -> None:
        pass

    async def push_fileref( self, fileref: LineRef ) -> None:
        if self.downstream:
            await self.downstream.accept_fileref(fileref)


LineParseFn: type = abc.Callable[ ParseContextBase , ParseContextBase ]

class ExecOpBase:

    def __init__( self: Self, name: str, _exec_fn: LineParseFn | None, bar: Bar | None ) -> None:
        self.name: str = name
        self._parse_fn: LineParseFn = _exec_fn or ExecOpBase.null_fn
        self.bar: Bar = bar or Bar(name)

    @property
    def parse_fn( self: Self ) -> LineParseFn:
        return self._parse_fn

    @parse_fn.setter
    def parse_fn( self: Self, fn: LineParseFn ) -> None:
        self._parse_fn = fn

#    def run( self: Self, line_ref: LineRef ) -> ParseResult:
#        return self._parse_fn( line_ref )

    def next( self: Self, val: int | None ) -> None:
        if val is not None:
            self.bar.next(val)
        else:
            self.bar.next()

    @staticmethod
    def null_fn(line_ref: LineRef) -> tuple[ParseState, str | None, Exception | None, str | None ]:
        print(f"[null_fn]  {line_ref}  ")
        return ParseState.UnknownErr, "", None, None

class StreamSourceOpBase(ExecOpBase):
    def __init__(self: Self, name: str, filepath: str) -> None:
        super(StreamSourceOpBase, self).__init__(
            name=name, _parse_fn=StreamSourceOpBase.do_parse
        )
        self.filepath = filepath
        self.file_id: TextIO | None = None

    @abstractmethod
    def open(self: Self) -> bool:
        pass

    @abstractmethod
    async def line_out(self: Self, line_ref: LineRef) -> bool:
        pass

    @abstractmethod
    def close(self: Self) -> None:
        if self.file_id is not None:
            self.file_id.close()

    @staticmethod
    def do_parse(line_ref: LineRef) -> bool:
        print(
            f"[FileReadOp.do_parse][{line_ref.file_id}:{line_ref.line_num}]  {line_ref.line}"
        )
        return True


class FileSourceOp( StreamSourceOpBase ):

    def __init__(self: Self, name: str,  filepath: str ) -> None:
        super( StreamSourceOpBase, self ).__init__( name=name, _parse_fn = StreamSourceOpBase.do_parse )
        self.filepath = filepath
        self.file_id: TextIO | None = None

    @abstractmethod
    def open( self: Self ) -> bool:
        try:
            self.file_id = open(self.filepath)
            return True

        except Exception as ext:
            print(f'[FileReadOp.open] Exception: {ext}')
            return False

    @abstractmethod
    async def line_out( self: Self, line_ref: LineRef ) -> bool:
        if self.file_id is not None:
            print(f'[FileReadOp.line_out][{line_ref.file_id}:{line_ref.line_num}]  {line_ref.line}')
            return True
        else:
            return False

    @abstractmethod
    def close( self: Self ) -> None:
        if self.file_id is not None:
            self.file_id.close()

    @staticmethod
    def do_parse(line_ref: LineRef) -> bool:
        print(f'[FileReadOp.do_parse][{line_ref.file_id}:{line_ref.line_num}]  {line_ref.line}')
        return True


class ExecCtxBase:

    def __init__(self: Self) -> None:
        self.cur_prompt: str
        self.op_list: list[ ExecOpBase ] = []

    def add_op(self: Self, op: ExecOpBase) -> None:
        self.op_list.append(op)

    def run(self: Self, line: str, line_nun: int) -> bool:
#        for op in self.op_list:
#            if not op.run((0, line_nun, line )):
#                return False

        return True




if __name__ == "__main__":

    exec_ctx = ExecCtxBase()





