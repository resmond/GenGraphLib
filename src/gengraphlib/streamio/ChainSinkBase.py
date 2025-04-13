from typing import Self

from collections.abc import AsyncGenerator

from src.gengraphlib import ChainableResult, PipedChain, PipeChainType

class ChainSinkBase[ T: ChainableResult ]( PipedChain[ T: ChainableResult ] ):
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

