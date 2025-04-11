from collections.abc import AsyncGenerator
from typing import Self

from sphinx.writers.text import TextWriter

from src.gengraphlib import KeyGraphDefBase, KeyValueSet
from src.gengraphlib.graph.GraphSlice import GraphSliceDef


class GraphRepositoryBase:

    def __init__(self: Self, keygraph_def: KeyGraphDefBase, key_slice: GraphSliceDef ):
        self._keygraph_def : KeyGraphDefBase = keygraph_def
        self._key_slice : GraphSliceDef = key_slice
        pass

    async def write_slice( self, value_source: AsyncGenerator[KeyValueSet, None, None ] ) -> bool:
        pass

class GraphFileRepository( GraphRepositoryBase ):

    def __init__(self: Self, keygraph_def: KeyGraphDefBase, key_slice: GraphSliceDef, file_path: str ):
        super().__init__(keygraph_def, key_slice)
        self._file_path : str = file_path
        self._file : TextWriter | None = None

    def open( self ) -> bool:
        try:
            self._file = open( self._file_path, "w" )
            return True
        except Exception as exc:
            print(exc)
            return False

    def close( self ) -> None:
        if self._file is not None:
            self._file.close()
            self._file = None

    async def write_slice( self, value_source: AsyncGenerator[KeyValueSet, None ] ) -> bool:
        async for value in value_source:
            await self._file.writelines( value.to_text() )



        return True






