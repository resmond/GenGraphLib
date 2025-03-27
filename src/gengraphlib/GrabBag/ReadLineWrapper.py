from typing import Self

import io
import _asyncio

class StringIteratorIO( io.TextIOBase ):

    def __init__(self: Self, iter) -> None:
        super().__init__()
        self._iter = iter
        self._left = ''

    def readable(self: Self) -> bool:
        return True

    def _read1( self: Self, max_len: int | None = None ):
        while not self._left:
            try:
                self._left = next(self._iter)
            except StopIteration:
                break
        ret = self._left[ :max_len ]
        self._left = self._left[len(ret):]
        return ret

    def read( self: Self, next_char_index=None ) -> str:
        str_list: list[str] = []
        if next_char_index is None or next_char_index < 0:
            while True:
                read_result = self._read1()
                if not read_result:
                    break
                str_list.append(read_result)
        else:
            while next_char_index > 0:
                read_result = self._read1( next_char_index )
                if not read_result:
                    break
                next_char_index -= len( read_result )
                str_list.append(read_result)
        return ''.join(str_list)

    def readline( self: Self, **kwargs ) -> str:
        str_list: list[str] = []
        while True:
            line_end = self._left.find('\n')
            if line_end == -1:
                str_list.append(self._left)
                try:
                    self._left = next(self._iter)
                except StopIteration:
                    self._left = ''
                    break
            else:
                str_list.append(self._left[:line_end+1])
                self._left = self._left[line_end+1:]
                break
        return ''.join(str_list)