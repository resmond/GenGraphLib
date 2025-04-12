from asyncio import Protocol
from collections.abc import AsyncGenerator
from enum import IntEnum
from typing import Self

from src.gengraphlib import ChainableResult

class PipeChainType(IntEnum):
    PipeSink     = 0x01
    PipeSource   = 0x02
    PipeFilter   = PipeSink | PipeSource

class PipedChainBase[ T: ChainableResult ]( Protocol ):
    pipechain_type: PipeChainType

    @property
    def chain( self: Self) -> AsyncGenerator[T, None] | None:
        return None

    @chain.setter
    def chain( self: Self, _source_pipe: AsyncGenerator[T, None ] | None ) -> None:
        pass

    def run_pipe(self: Self ) -> T | None:
        pass





