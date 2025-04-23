from dataclasses import dataclass, field
from typing import Self

from ..common import KeyType
from ..bootlog.BootLogInfo import BootLogInfo

@dataclass
class KeyInfo:
    schema_id: str
    key: str
    alias: str
    keytype: KeyType
    groupids: list[str] = field(default_factory=list)

    @property
    def keyinfo_id( self: Self ) -> str:
        return f"{self.schema_id}@{self.key}"

@dataclass
class KeyValSchemaInfo:
    bootlog_info:  BootLogInfo
    keys:          list[KeyInfo]
    groups:        list[str]
    active_groups: list[str] | None = None
    active_keys:   list[str] | None = None

