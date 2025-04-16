from typing import Self

from .. import DataMsg

class IndexingProgressMsg(DataMsg):

    def __init__(self: Self, key: bytes, value: bytes) -> None:
        super(IndexingProgressMsg, self).__init__(key, value)
