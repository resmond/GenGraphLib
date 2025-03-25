from __future__ import annotations

from collections.abc import Callable
from enum import IntEnum

from typing import  Self, TypedDict, TypeVar, Any

class ResultState(IntEnum):
    Found = 1
    NoneFound = 0
    ParseError = -1
    Exception = -2

class ParseTestResult(TypedDict):
    state: ResultState
    values: dict

TParseTestFn = TypeVar( "TParseTestFn", bound = Callable[ [ str, str], ParseTestResult ] )

class ParseTrigger:

    def __init__(self: Self, tag: str, match_phrase: str, parse_fn: TParseTestFn) -> None:
        self.tag: str = tag
        self.match_phrase: str = match_phrase
        self.parse_fn: TParseTestFn = parse_fn

    def parseif( self: Self, parse_str: str ) -> ParseTestResult | None:
        if parse_str.find(self.match_phrase) != -1:
            return self.parse_fn( parse_str )
        else:
            return None

    @staticmethod
    def defautl_fn( input_str: str ) -> ParseTestResult | None:
        return ParseTestResult( state=ResultState.NoneFound, values={"message": input_str} )

class ParseTriggers( dict[ str, ParseTrigger ] ):

    def __init__( self: Self ) -> None:
        super(ParseTriggers, self).__init__()

    def execute( self: Self, input_str: str ) -> ParseTestResult:
        results: dict[ str, Any ] | None = None
        result: ParseTestResult = ParseTestResult( state=ResultState.NoneFound, values={"message": input_str} )
        for key, trigger in self.items():
            phrase: str = self[ key ].match_phrase
            tag: str = self[ key ].tag

            if input_str.find( phrase ) != -1:
                result = self[ key ].parse_fn( "", input_str )

                match result["state"]:
                    case ResultState.NoneFound:
                        results[ tag ] = result.values
                        print( f'Success on [{phrase}]=({tag}): {input_str}' )
                        print( f'    {result.values}' )
                        print()

                    case ResultState.ParseError:
                        print( f'ParseError on [{phrase}]: {input_str}' )

                    case ResultState.Exception:
                        print( f'Exception on [{phrase}]: {input_str}' )

                    case _:
                        print( f'Otherwise on [{phrase}]: {input_str}' )

        return result
