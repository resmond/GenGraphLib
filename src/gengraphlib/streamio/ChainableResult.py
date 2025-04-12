from abc import ABC
from enum import IntEnum
from typing import Self

class ChainedResultErr( IntEnum ):
    Success         = 0
    FileReaderError = -1
    FileWriterError = -2
    ParsingError    = -3
    UnexpectedError = -99
    
class ResultChainException(Exception):
    def __init__( self, error_val: ChainedResultErr ):
        super().__init__()
        self.error_val: ChainedResultErr = ChainedResultErr.UnexpectedError

class KeyValueResultErr( ChainedResultErr ):
    UnknownKey = -10

class KeyValueResultException(ResultChainException):
    def __init__( self, error_val: KeyValueResultErr ):
        super().__init__(error_val)
        self.error_val: ChainedResultErr = ChainedResultErr.UnexpectedError

class ChainableResult( ABC ):
    def __init__(self: Self) -> None:
        super().__init__()
        self.error_val: ChainedResultErr = ChainedResultErr.Success





if __name__ == "__main__":
    test_list = [1, 2, 3]

    first, second, third, fourth, fifth = test_list

    print(first)
    print(second)
    print(third)
    print(fourth)
    print(fifth)
    pass




