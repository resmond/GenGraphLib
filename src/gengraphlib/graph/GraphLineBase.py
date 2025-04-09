from typing import Self

from .GraphNodeLib import GraphNodeBase

class GraphLineBase( GraphNodeBase ):

    def __init__(self: Self, line_str: str, line_num: int) -> None:
        self.line_str: str = line_str
        self.line_num: int = line_num
        super().__init__(str(line_num))

