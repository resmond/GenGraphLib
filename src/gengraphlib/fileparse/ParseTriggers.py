from __future__ import annotations

from typing import  Self
from collections.abc import Callable
from dataclasses import dataclass
from enum import IntEnum

class ResultState(IntEnum):
    Found = 1
    NoneFound = 0
    ParseError = -1
    Exception = -2

@dataclass
class LineParseResult:
    state: ResultState | None = None
    tag: str | None = None
    message: str | None = None
    exception: Exception | None = None
    #values: dict

TParseTestFn = Callable[ [ str, str], LineParseResult ]

class ParseTrigger:

    def __init__(self: Self, tag: str, match_phrase: str, parse_fn: TParseTestFn) -> None:
        self.tag: str = tag
        self.match_phrase: str = match_phrase
        self.parse_fn: TParseTestFn = parse_fn

    def parseif( self: Self, parse_str: str ) -> LineParseResult | None:
        if parse_str.find(self.match_phrase) != -1:
            return self.parse_fn( parse_str )
        else:
            return None

    @staticmethod
    def defautl_fn( input_str: str ) -> LineParseResult | None:
        return LineParseResult( state=ResultState.NoneFound, message=input_str )

class ParseTriggers( dict[ str, ParseTrigger ] ):

    def __init__( self: Self ) -> None:
        super(ParseTriggers, self).__init__()

    def execute( self: Self, input_str: str ) -> LineParseResult:
        result: LineParseResult = LineParseResult( state=ResultState.NoneFound, message=input_str )
        for key, trigger in self.items():
            phrase: str = self[ key ].match_phrase

            if input_str.find( phrase ) != -1:
                result = self[ key ].parse_fn( "", input_str )
                result.tag = self[key].tag

        return result
