from typing import Self
from enum import IntEnum

from asyncio import Protocol, Queue
from collections.abc import AsyncGenerator

class ChainErr( IntEnum ):
    Success         = 0
    FileReaderError = -1
    FileWriterError = -2
    ParsingError    = -3
    UnexpectedError = -99

class PipeChainType(IntEnum):
    PipeError    = 0x00
    PipeSink     = 0x01
    PipeSource   = 0x02
    PipeFilter   = PipeSink | PipeSource

class StreamType(IntEnum):
    Binary = 0
    NullTextLine = 1
    LfTextLine = 2
    CrLfTextLine = 3

class ChainException( Exception ):
    def __init__( self, chain_err: ChainErr = ChainErr.UnexpectedError ):
        super().__init__()
        self.error_val: ChainErr = chain_err

class PartialResult:
    def __init__( self: Self, buf: bytes | None = None ) -> None:
        super().__init__()
        self._buffer: bytes = buf

    @property
    def buffer_size(self: Self) -> int:
        if self.buffer is not None:
            return len(self._buffer)
        else:
            return 0

    @property
    def buffer(self: Self) -> bytes | None:
        return self._buffer

    # @buffer.setter
    # def buffer(self: Self, buffer: bytes) -> None:
    #     self._buffer = buffer

class ChainableResult( list[bytes] ):

    def __init__( self: Self, buf: bytes | None = None ) -> None:
        super(ChainableResult, self).__init__()
        self.error_val: ChainErr = ChainErr.Success
        self.exc: Exception | None = None
        if buf is not None:
            self.append(buf)

    def set_error( self: Self, error_val: ChainErr ) -> None:
        self.error_val = error_val

    def set_exception( self: Self, exc: Exception ) -> None:
        self.exc = exc

    def add_buffer( self: Self, buffer: bytes ) -> None:
        self.append( buffer )

    def dequeue( self: Self ) -> bytes | None:
        return self.pop()

class PipedChainBase[ T: ChainableResult ]( Protocol ):
    pipechain_type: PipeChainType

    @property
    def chain_type( self: Self ) -> PipeChainType:
        return self.pipechain_type

    @property
    def chain( self: Self) -> AsyncGenerator[T, None] | None:
        return None

    @chain.setter
    def chain( self: Self, _source_pipe: AsyncGenerator[T, None ] | None ) -> None:
        pass

    def run_pipe(self: Self ) -> AsyncGenerator[T, None ] | None | None:
        pass

class ChainSourceBase[ T: ChainableResult ]( PipedChainBase[ T: ChainableResult ] ):
    pipechain_type: PipeChainType.PipeSource

    def __init__( self: Self, stream_type: StreamType = StreamType.LfTextLine, buffer_size: int = 4096 ) -> None:
        super( ChainSourceBase, self ).__init__()
        self.stream_type: StreamType = stream_type
        self.buffer_size: int = buffer_size

    @property
    def chain( self: Self) -> AsyncGenerator[T, None] | None:
        return self

    @chain.setter
    def chain( self: Self, _source_pipe: AsyncGenerator[T, None ] | None ) -> None:
        pass

    async def run_pipe(self: Self) -> T | None:
        return await self._new_result()

    async def _new_result( self: Self ) -> T | None:
        pass

class ChainFilterBase[ T: ChainableResult ]( PipedChainBase[ T:ChainableResult ] ):
    pipechain_type: PipeChainType.PipeFilter

    def __init__(self: Self):
        super( ChainFilterBase, self ).__init__()
        self.source_pipe: AsyncGenerator[T, None ] | None = None
        self.null_result: T | None = None

    @property
    def chain( self: Self) -> AsyncGenerator[T, None] | None:
        return self

    @chain.setter
    def chain( self: Self, _source_pipe: AsyncGenerator[T, None ] | None ) -> None:
        self.source_pipe = _source_pipe

    async def run_pipe( self: Self ) -> T | None:
        if self.source_pipe is not None:
            async for chain_result in self.source_pipe:
                return await self._filter_result( chain_result )

        return None

    async def _filter_result( self: Self, input_result: T ) -> T | None:
        if input_result is None:
            return self.null_result
        else:
            return input_result

class ChainSinkBase[ T: ChainableResult ]( PipedChainBase[ T: ChainableResult ] ):
    pipechain_type: PipeChainType.PipeSink

    def __init__(self: Self) -> None:
        super( ChainSinkBase, self ).__init__()
        self.source_pipe: AsyncGenerator[T, None ] | None = None

    @property
    def chain( self: Self) -> AsyncGenerator[T, None] | None:
        return None

    @chain.setter
    def chain( self: Self, _source_pipe: AsyncGenerator[T, None ] | None ) -> None:
        self.source_pipe = _source_pipe

    async def run_pipe(self: Self ) -> T | None:
        if self.source_pipe is not None:
            async for chain_result in self.source_pipe:
                await self._sink_result( chain_result )

        return None

    async def _sink_result( self, chain_result: T | None) -> None:
        pass










