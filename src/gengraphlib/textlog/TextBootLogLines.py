from typing import Self, Any

from src.gengraphlib import GraphNodeBase, RecordBase, LineParseResult, ResultState, RgxLine

class TextBootLogLine( RecordBase ):

    def __init__( self: Self, _graph_root: Any, line_str: str, rec_index: int ) -> None:
        super().__init__( _graph_root, rec_index = rec_index, line_str = line_str )
        self.rgx_line: RgxLine = RgxLine()
        self.event_type_id: str = ""
        self.date_seg: str = ""
        self.machine: str = ""
        self.thread_id: str = ""
        self.module_type_id: str = ""
        self.module_id: str = ""
        self.message: str = ""
        #self.values: dict[str, str] | None = None

    def parse_line( self: Self, event_type_id: str, field_values: dict[str, str] ) -> LineParseResult:
        self.event_type_id = event_type_id

        result_state: ResultState = ResultState.NoneFound
        try:
            self.date_seg = field_values[ "date_seg" ]
            self.machine = field_values[ "machine" ]
            self.thread_id = field_values[ "thread_id" ]
            self.module_type_id = field_values[ "module_type_id" ]
            self.module_id = field_values[ "module_id" ]
            self.message = field_values[ "message" ]

        except Exception as exc:
            print(f"error: {self.line_str}")
            print(f"dict: {field_values}" )
            print(f"Eception:{exc}")
            result_state = ResultState.Exception

        return LineParseResult( state=result_state, message = field_values[ "message" ] )

class TextBootLogLines( GraphNodeBase, list[TextBootLogLine ] ):

    def __init__( self: Self, _graph_root: Any ) -> None:
        #self.log_file_graph: LogFileGraph
        self.cnt: int = 0
        self._graph_root: Any = _graph_root
        super().__init__( id= "lineNodeIndex" )

    def new_line( self: Self, line_str: str, line_num: int ) -> TextBootLogLine:
        new_line: TextBootLogLine =  TextBootLogLine( self._graph_root, line_str=line_str, rec_index =line_num )
        self.append( new_line )
        return new_line

    def __add__( self, other: TextBootLogLine ) -> None:
        self.append(other)



