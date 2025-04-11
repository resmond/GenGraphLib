from collections.abc import AsyncGenerator
from io import TextIOWrapper
from typing import Self

from src.gengraphlib import KeyGraphBase, KeyValues
from src.gengraphlib.graph.GraphView import GraphView


class GraphRepositoryBase:

    def __init__( self: Self, keygraph_def: KeyGraphBase, key_slice: GraphView ):
        self._keygraph_def : KeyGraphBase = keygraph_def
        self._key_slice : GraphView = key_slice
        pass

    async def write_slice( self, value_source: AsyncGenerator[KeyValues, None, None ] ) -> bool:
        pass

class GraphFileRepository( GraphRepositoryBase ):

    def __init__( self: Self, keygraph_def: KeyGraphBase, key_slice: GraphView, file_path: str ):
        super().__init__(keygraph_def, key_slice)
        self._file_path : str = file_path
        self._file : TextIOWrapper | None = None

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

    async def write_slice( self, value_source: AsyncGenerator[KeyValues, None ] ) -> bool:
        async for value in value_source:
            pass
            #value
            #await self._file.writelines( [  ] )



        return True






