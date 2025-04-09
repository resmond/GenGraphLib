from typing import Self

from .GraphNodeLib import GraphNodeBase

class GraphLineBase( GraphNodeBase ):

    def __init__(self: Self, line_str: str, line_num: int) -> None:
        super().__init__( line_str = line_str, line_num = line_num )

