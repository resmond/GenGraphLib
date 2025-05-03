from dataclasses import dataclass

from enum import IntEnum

class KeyType(IntEnum):
    StrKey = 1
    IntKey = 2
    ListKeys = 3
    RelativeTimeSeries = 4

@dataclass
class KeyRec:
    key: str
    journal_key: str


