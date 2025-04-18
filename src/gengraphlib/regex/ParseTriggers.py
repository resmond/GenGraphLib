from typing import  Self

from collections.abc import Callable
from dataclasses import dataclass
from enum import IntEnum

class ResultState(IntEnum):
    Found = 1
    NoneFound = 0
    ParseError = -1
    Exception = -2

class TriggerType(IntEnum):
    Scan = 1
    RegEx = 2
    LeadWhitespace = 3

@dataclass
class LineParseResult:
    type: TriggerType = TriggerType.Scan
    state: ResultState | None = None
    tag: str | None = None
    message: str | None = None
    exception: Exception | None = None
    #values: dict

TParseTestFn = Callable[ [str, str], LineParseResult ]

class MatchTrigger:

    def __init__(self: Self, tag: str, match_phrase: str, parse_fn: TParseTestFn) -> None:
        super().__init__()
        self.tag: str = tag
        self.match_phrase: str = match_phrase
        self.parse_fn: TParseTestFn = parse_fn

    def parseif( self: Self, parse_str: str ) -> LineParseResult | None:
        if parse_str.find(self.match_phrase) != -1:
            return self.parse_fn( "", parse_str )
        else:
            return None

    @staticmethod
    def defautl_fn( input_str: str ) -> LineParseResult | None:
        return LineParseResult( state=ResultState.NoneFound, message=input_str )

class ParseTriggers( dict[ str, MatchTrigger ] ):

    def __init__( self: Self ) -> None:
        super().__init__()

    def execute( self: Self, input_str: str ) -> LineParseResult:
        result: LineParseResult = LineParseResult( state=ResultState.NoneFound, message=input_str )
        for key, trigger in self.items():
            match trigger.type:

                case TriggerType.Scan:
                    phrase: str = self[ key ].match_phrase
                    if input_str.find( phrase ) != -1:
                        result = self[ key ].parse_fn( "", input_str )
                        result.tag = self[key].tag

                case TriggerType.RegEx:
                    pass

                case TriggerType.LeadWhitespace:
                    if input_str.startswith( " " ):
                        result = self[ key ].parse_fn( "", input_str )

        return result
