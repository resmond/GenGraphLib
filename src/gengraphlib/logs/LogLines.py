from typing import Self

from ..fileparse.GNodeLib import NodeBase
from ..fileparse.ParseTriggers import LineParseResult, ResultState
from ..fileparse.RgxCore import RgxLine

class LogLine( NodeBase ):

    def __init__(self: Self, line_str: str, line_num: int) -> None:
        super( LogLine, self ).__init__( line_str = line_str, line_num = line_num )
        self.rgx_line: RgxLine = RgxLine()
        self.event_type_id: str = ""
        self.date_seg: str = ""
        self.machine: str = ""
        self.thread_id: str = ""
        self.module_type_id: str = ""
        self.module_id: str = ""
        self.message: str = ""
        #self.values: dict[str, str] | None = None

    def parse_line( self: Self, event_type_id: str, field_values: dict[str, str ] ) -> LineParseResult:
        self.event_type_id = event_type_id

        result_state: ResultState = ResultState.NoneFound
        try:
            self.date_seg = field_values[ "date_seg" ]
            self.machine = field_values[ "machine" ]
            self.thread_id = field_values[ "thread_id" ]
            self.module_type_id = field_values[ "module_type_id" ]
            self.module_id = field_values[ "module_id" ]
            self.message = field_values[ "message" ]

        except Exception as e:
            print(f"error: {self.line_str}")
            print(f"dict: {field_values}" )
            print(f"Eception:{e}")
            result_state = ResultState.Exception

        return LineParseResult( state=result_state, message = field_values[ "message" ] )

class LogLines( NodeBase, list[LogLine] ):

    def __init__( self: Self ) -> None:
        #self.log_file_graph: LogFileGraph
        self.cnt: int = 0
        super( LogLines, self ).__init__( id= "lineNodeIndex" )

    def new_line( self: Self, line_str: str, line_num: int ) -> LogLine:
        new_line: LogLine =  LogLine( line_str=line_str, line_num=line_num )
        self.append( new_line )
        return new_line

    def __add__( self, other: LogLine ) -> None:
        self.append(other)



