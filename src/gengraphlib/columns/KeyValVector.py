from collections import namedtuple
from collections.abc import Iterable
# from dataclasses import dataclass, field
# from enum import IntEnum
from typing import Self

import pickle as pk

from src.gengraphlib.common import KeyValTypes, KeyInfo, VectorValTypes

class KeyValVector:

    def __init__( self: Self, vec_name: str, keys: list[KeyInfo] ) -> None:
        super( KeyValVector, self ).__init__()
        self.vec_name: str = vec_name
        self._keys: list[KeyInfo] = keys
        self.key_cnt: int = len(keys)
        self.cur_vals: list[VectorValTypes] = [None] * self.key_cnt

        index: int = -1
        self.key_map: dict[str,int] = { info.key:++index for info in self._keys }
        self.vec_fieldnames: list[str] = [ info.key for info in keys ]
        self.named_tuple: type = namedtuple(self.vec_name, self.field_names )

    def setval( self: Self, key: str, value: KeyValTypes ) -> None:
        self.cur_vals[ self.key_map[ key ] ] = value

    def to_tuples( self: Self ) -> tuple:
        return tuple( self.cur_vals )

    def tup_binary( self: Self ) -> bytes:
        buffer: bytes = pk.dumps( tuple( self.cur_vals ) )
        return buffer

    def list_binary( self: Self ) -> bytes:
        buffer: bytes = pk.dumps( self.cur_vals )
        return buffer

    def to_namedtuple( self: Self ) -> namedtuple:
        new_named_tuple = self.named_tuple( self.vec_values )
        return new_named_tuple

    def get_delimated_header( self: Self ) -> str:
        return ",".join(self.vec_fieldnames)

    def to_delimited( self: Self ) -> str:
        return ",".join(self.cur_vals)


class VectorResult:

    def __init__( self: Self, _iter: Iterable[ tuple[ str, KeyValTypes ] ] ):
        super().__init__()
        self.__dict__ = { key:value for key,value in vec_iter }


if __name__ == "__main__":

    vec_vals: dict[ str, KeyValTypes ] = { "x": "foo", "y": "bar", "k": 5 }

    vec_iter: Iterable[ tuple[ str, KeyValTypes ] ] = (
        ( "x", "foo" ),
        ( "y", "bar" ),
        ( "k", 5     )
    )

    vec_dict: dict = { key:value for key,value in vec_iter }

    vec_result: VectorResult = VectorResult( _iter=vec_iter )

    print( vec_result )
