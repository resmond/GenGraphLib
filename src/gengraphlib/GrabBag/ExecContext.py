from abc import abstractmethod
from enum import IntEnum
from typing import Self, TextIO
import collections.abc as abc
from typing_extensions import NamedTuple

from progress.bar import Bar

class ParseErrType(IntEnum):
    Success      = 0
    Unknown      = -1
    OpenErr      = -2
    StdException = -3

class PrsReslt(NamedTuple):
    err: ParseErrType = ParseErrType.Success
    clsnm: str | None = None
    exc: Exception | None = None
    msg: str | None = None

    def __bool__(self) -> bool:
        return self.err != ParseErrType.Success

LineRef = NamedTuple("LineRef", [ ("file_id", int),("line_num", int), ("line", str) ] )
LineParseFn: type = abc.Callable[ LineRef , bool ]

def test_print( line_ref: LineRef ) -> bool:
    file_id = line_ref.file_id
    line_num = line_ref.line_num
    line = line_ref.line
    print(f'[test_print: ({file_id}:{line_num})]  {line}' )
    return True



class ExecOpBase:

    def __init__( self: Self, name: str, _parse_fn: LineParseFn | None, bar: Bar | None ) -> None:
        self.name: str = name
        self._parse_fn: LineParseFn = _parse_fn or ExecOpBase.null_fn
        self.bar: Bar = bar or Bar(name)

    @property
    def parse_fn( self: Self ) -> LineParseFn:
        return self._parse_fn

    @parse_fn.setter
    def parse_fn( self: Self, fn: LineParseFn ) -> None:
        self._parse_fn = fn

    def run( self: Self, line_ref: LineRef ) -> bool:
        return self._parse_fn( line_ref )

    def next( self: Self, val: int | None ) -> None:
        if val is not None:
            self.bar.next(val)
        else:
            self.bar.next()

    @staticmethod
    def null_fn(line_ref: LineRef) -> bool:
        print(f"[null_fn]  {line_ref}  ")
        return False

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
        for op in self.op_list:
            if not op.run((0, line_nun, line )):
                return False

        return True


if __name__ == "__main__":

    exec_ctx = ExecCtxBase()





