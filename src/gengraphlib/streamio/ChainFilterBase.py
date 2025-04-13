from typing import Self

from collections.abc import AsyncGenerator

from src.gengraphlib import ChainableResult, PipedChain, PipeChainType

class ChainFilterBase[ T: ChainableResult ]( PipedChain[ T:ChainableResult ] ):
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

    async def run_pipe(self: Self ) -> T | None:
        if self.source_pipe is not None:
            async for chain_result in self.source_pipe:
                return await self._filter_result( chain_result )

        return None

    async def _filter_result( self: Self, input_result: T ) -> T | None:
        if input_result is None:
            return self.null_result
        else:
            return input_result
