from abc import ABC, abstractmethod
from typing import Self, AsyncGenerator

import asyncio as aio

from src.gengraphlib import KeyValueSchema, KeyValues, GraphVector


#class FileChainSource( ChainSourceBase ): ...

class GraphFileBase( ABC ):

    def __init__( self: Self, _schema: KeyValueSchema, _vector: GraphVector, file_path: str ):
        super().__init__()
        self._schema: KeyValueSchema = _schema
        self._vector: GraphVector = _vector
        self._file_path : str = file_path

    @abstractmethod
    def open( self ) -> bool:
        pass

    @abstractmethod
    def close( self ) -> None:
        pass

class GraphFileSource( GraphFileBase ):
    def __init__( self: Self, key_graph: KeyValueSchema, _vector: GraphVector, file_path: str ):
        super().__init__( key_graph, _vector, file_path )
        self.input_stream : aio.StreamReader | None = None

    def open( self ) -> bool:
        try:
            self.input_stream = open( self._file_path, "rb" )
            return True
        except Exception as exc:
            print(exc)
            return False

    def close( self ) -> None:
        self.input_stream = None

    async def stream_values( self ) -> AsyncGenerator[KeyValues, None ]:
        pass
#        key_values: list[KeyValues] = []
#        async for value in key_values:
#            yield value

class GraphFileSink( GraphFileBase ):

    def __init__( self: Self, key_graph: KeyValueSchema, _vector: GraphVector, file_path: str ):
        super(GraphFileSink, self).__init__( key_graph, _vector, file_path )
        self.output_stream : aio.StreamWriter | None = None
        self.value_source: AsyncGenerator[KeyValues, None ] | None

    def open( self: Self ) -> bool:
        try:
            self.output_stream = open( self._file_path, "wb" )
            return True
        except Exception as exc:
            print(exc)
            return False

    def pipe_in( self: Self, value_source: AsyncGenerator[KeyValues, None ] | None ) -> AsyncGenerator[KeyValues, None ] | None:
        pass

    def pipe_out( self: Self, value_source: AsyncGenerator[KeyValues, None ] | None ) -> AsyncGenerator[KeyValues, None ] | None:
        pass

    async def loop_chain( self: Self ) -> bool:
        if self.value_source is not None:

            if self.output_stream is not None or self.open():

                async for value in self.value_source:
                    binary_data: bytes = str(value).encode()
                    self.output_stream.write(binary_data)

                return True

        return False

    def close( self: Self ) -> None:
        if self.output_stream is not None:
            self.output_stream.close()
            self.output_stream = None
