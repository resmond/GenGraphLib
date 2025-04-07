from typing import Self

from collections.abc import Iterable, Mapping, Sequence

from typing_extensions import Protocol

from .KeyDefs import KeyDefBase


class KeyLookup[T: KeyDefBase](Mapping[str], Sequence[T]):

    def __getitem__( self, key, / ):
        pass

    def __len__( self ):
        pass