from typing import Self

from collections.abc import AsyncGenerator

from src.gengraphlib import ChainableResult, PipedChainBase, PipeChainType


class ChainSourceBase[ T: ChainableResult ]( PipedChainBase[ T: ChainableResult ] ):
    pipechain_type: PipeChainType.PipeSource

    def __init__( self: Self) -> None:
        super( ChainSourceBase, self ).__init__()
        #self.sink_pipe: AsyncGenerator[T, None ] | None = None

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
