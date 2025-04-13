from abc import ABC
from enum import IntEnum
from typing import Self

class ChainErr( IntEnum ):
    Success         = 0
    FileReaderError = -1
    FileWriterError = -2
    ParsingError    = -3
    UnexpectedError = -99
    
class ChainException( Exception ):
    def __init__( self, error_val: ChainErr ):
        super().__init__()
        self.error_val: ChainErr = ChainErr.UnexpectedError

class ChainableResult( ABC ):
    def __init__(self: Self) -> None:
        super().__init__()
        self.error_val: ChainErr = ChainErr.Success





if __name__ == "__main__":
    test_list = [1, 2, 3]

    first, second, third, fourth, fifth = test_list

    print(first)
    print(second)
    print(third)
    print(fourth)
    print(fifth)
    pass




