from typing import Self


class ParseStateMachine:

    def __init__( self: Self ) -> None:
        self.state: int = 0

    def parse( self: Self, chars: bytes ):

        c = 0b10000000

        if (


        for c  in chars:
            flip_bit: bool =
            match c:
                case c > 0x7f:


