from typing import Self

from collections.abc import Callable

from .. import GraphRecordRoot

dispatch_fn: Callable[str, None] | None = None

class KeyValueDispatcher( dict[ bytes, dispatch_fn ] ):

    def __init__(self: Self, key_schema: GraphRecordRoot ):
        super(KeyValueDispatcher, self).__init__()
        self.key_schema: GraphRecordRoot = key_schema

