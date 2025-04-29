from typing import Self
import multiprocessing as mp
import datetime as dt

import pyarrow as par

from ..common import KeyType, KeyValTypes, KeyDefInterface, KeyInfo

class KeyDefBase[T: KeyValTypes ]( KeyDefInterface ):
    def __init__( self: Self, key: str, alias: str, keytype: KeyType, partype: par.DataType, groups: list[ str ] | str | None = None ) -> None:
        super(KeyDefBase, self).__init__()
        self.key:            str  = key
        self.alias:          str  = alias
        self.keytype:       KeyType = keytype
        self.pytype:         type = type(T)
        self.partype: par.DataType = partype
        self.groupids:       list[str] = []
        self._skip:          bool = True
        self._event_trigger: bool = False

        #self.key_values: Column[ T ] = Column[ T ]( self, "" )

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

    def get_keyinfo( self: Self ) -> KeyInfo:
        return KeyInfo(
            keytype=self.keytype,
            pytype=self.pytype,
            partype=self.partype,
            key=self.key,
            alias=self.alias,
            groupids=self.groupids
        )

    def visit( self: Self, visitor ) -> None:
        visitor.visit_key_def( self )

class StrKeyDef( KeyDefBase[str] ):
    def __init__( self: Self, key: str, alias: str, groups: list[str ] | str | None = None ) -> None:
        super(StrKeyDef, self).__init__( key=key, alias=alias, keytype=KeyType.KStr, partype=par.utf8(), groups=groups )

class IntKeyDef( KeyDefBase[int] ):
    def __init__( self: Self, key: str, alias: str, groups: list[str ] | str | None = None ) -> None:
        super(IntKeyDef, self).__init__( key=key, alias=alias, keytype=KeyType.KInt, partype=par.int64(), groups=groups )

class BoolKeyDef( KeyDefBase[bool] ):
    def __init__( self: Self, key: str, alias: str, groups: list[str ] | str | None = None ) -> None:
        super(BoolKeyDef, self).__init__( key=key, alias=alias, keytype=KeyType.KBool, partype=par.uint8(), groups=groups )

class TmstKeyDef( KeyDefBase[ dt.datetime ] ):
    very_beginning = dt.datetime.fromisoformat("1970-01-01")

    def __init__( self, key: str, alias: str, groups: list[str ] | str | None = None ) -> None:
        super(TmstKeyDef, self).__init__( key=key, alias=alias, keytype=KeyType.KTmst, partype=par.date32(), groups=groups )

class FloatKeyDef( KeyDefBase[float] ):
    def __init__( self, key: str, alias: str, groups: list[str ] | str | None = None ) -> None:
        super(FloatKeyDef, self).__init__( key=key, alias=alias, keytype=KeyType.KFloat, partype=par.int64(), groups=groups )

class KeyDefDict( dict[ str, KeyDefBase ] ):
    def __init__( self: Self ) -> None:
        super( KeyDefDict, self ).__init__()
