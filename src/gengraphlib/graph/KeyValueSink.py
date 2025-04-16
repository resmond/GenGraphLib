from typing import Self

import multiprocessing as mp

from src.gengraphlib import KeyDefBase, KeyValTypes

class KeyValueSink[ T: KeyValTypes ]:

    def __init__(self: Self, key_def: KeyDefBase ) -> None:
        self.key_def: KeyDefBase = key_def
        self.mp_queue: mp.Queue = mp.Queue(4096)

    async def async_accept( self, value_buffer: bytes ) -> None:
        pass

    async def apply_value( self, value: T ):
        pass



