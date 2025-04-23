from typing import Self
import multiprocessing as mp

import datetime as dt

from ..common import KeyType, KeyValTypes, KeyDefInterface
from .KeyValues import KeyValues
from .KeyValSchemaInfo import KeyInfo

#from ..proc.AppProcessBase import AppProcessBase

class KeyDefBase[T: KeyValTypes ]( KeyDefInterface ):
    def __init__( self: Self, key: str, alias: str, key_type: KeyType, groups: list[str ] | str | None = None ) -> None:
        super(KeyDefBase, self).__init__()
        self.key:            str = key
        self.alias:          str = alias
        self._skip:          bool = True
        self._event_trigger: bool = False
        self.key_type:       KeyType = key_type
        self.groupids:       list[str] | None = None

        self.key_values: KeyValues[T] = KeyValues[T]( self, "" )
        self._queue: mp.Queue | None = None

        match groups:
            case str() if groups in ["noise", ""]:
                pass
            case str():
                self.groupids = [ groups ]
                self._skip = False
            case [] if len(groups) > 0:
                self.groupids = groups
                self._skip = False

    @property
    def dologing( self: Self ) -> bool:
        return not self._skip

    def in_group( self: Self, group_id: str ) -> bool:
        if self.groupids is None:
            return False
        else:
            return group_id in self.groupids

    def queue( self: Self ) -> mp.Queue:
        self._queue = mp.Queue()
        return self._queue

    def get_keyinfo( self: Self, schema_id: str ) -> KeyInfo:
        return KeyInfo( schema_id=f"{schema_id}@{self.key}", key=self.key, alias=self.alias, keytype=self.key_type, groupids=self.groupids )

    def visit( self: Self, visitor ) -> None:
        visitor.visit_key_def( self )



class StrKeyDef( KeyDefBase[str] ):
    def __init__( self: Self, key: str, alias: str, groups: list[str ] | str | None = None ) -> None:
        super(StrKeyDef, self).__init__( key, alias, KeyType.KStr, groups )

class IntKeyDef( KeyDefBase[int] ):
    def __init__( self: Self, key: str, alias: str, groups: list[str ] | str | None = None ) -> None:
        super(IntKeyDef, self).__init__( key, alias, KeyType.KInt, groups )


class BoolKeyDef( KeyDefBase[bool] ):
    def __init__( self: Self, key: str, alias: str, groups: list[str ] | str | None = None ) -> None:
        super(BoolKeyDef, self).__init__( key, alias, KeyType.KBool, groups )

class TmstKeyDef( KeyDefBase[ dt.datetime ] ):
    very_beginning = dt.datetime.fromisoformat("1970-01-01")

    def __init__( self, key: str, alias: str, groups: list[str ] | str | None = None ) -> None:
        super(TmstKeyDef, self).__init__( key, alias, KeyType.KTmst, groups )

class FloatKeyDef( KeyDefBase[float] ):
    def __init__( self, key: str, alias: str, groups: list[str ] | str | None = None ) -> None:
        super(FloatKeyDef, self).__init__( key, alias, KeyType.KFloat, groups )


class KeyDict( dict[str, KeyDefBase ] ):
    def __init__( self: Self ) -> None:
        super(KeyDict, self).__init__()
