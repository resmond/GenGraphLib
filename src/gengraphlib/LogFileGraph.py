import json

from typing import Self, TextIO

#from fileparse.FileParse import FileParseContext
from fileparse.FileParse import FileParseContext
from fileparse.RgxCore import RgxLine, TRgxField
from fileparse.ParseTriggers import ParseTriggers, ParseTestResult
from LogNodes import LogLineNode, LineNodeIndex, ModuleTypeDict

patterns: dict[str, TRgxField ] = {
    "date_seg": TRgxField( r"^\w*\s\w*\s\w*:\w*:\w*", tail= " " ),
    "machine": TRgxField( r"\w*\S*", tail= " " ),
    "thread_id": TRgxField( r"\w*\[\w*\]", tail= ": " ),
    "module_id": TRgxField( r"\w*-\w*", tail= "." ),
    "module_type_id": TRgxField( r"\w*", tail= " - " ),
    "message": TRgxField( r".*" ),
}

class LogFileGraph:

    def __init__( self: Self, input_file_name: str, output_file_name: str ) -> None:
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.file_context: FileParseContext | None = None
        self.rgx_line: RgxLine = RgxLine()
        self.parse_triggers: ParseTriggers = ParseTriggers()

        self.lines: LineNodeIndex = LineNodeIndex()

        self.module_types: ModuleTypeDict = ModuleTypeDict()

#        self.event_types["unmet"] = EventTypeBase( id= "unmet", match_phrase = "unmet condition" )
#        from graphparse import EventTypeDict
#        self.event_types: EventTypeDict = EventTypeDict()

        self.next_line_number: int = 0

        self.init()

    def init( self: Self ) -> bool:
        self.file_context = FileParseContext( self.input_file_name, self.output_file_name, self.process_line )
        self.rgx_line.add_fields(patterns)

#        for event_type_id in self.event_types:
#            event_type: event_type = self.event_types[event_type_id]
#            self.parse_triggers[ event_type_id ] = ParseTrigger( tag= event_type.id, match_phrase = event_type.match_phrase, parse_fn = self.process_event )

        return True

    def process_line( self: Self, new_line_str: str ) -> ParseTestResult:
        parse_test_result: ParseTestResult = self.parse_triggers.execute( input_str= new_line_str )

        return parse_test_result

    def process_event( self: Self, event_type_id: str, new_line_str: str ) -> ParseTestResult:

#        if parse_test_result is not None and parse_test_result[ "state" ] == ResultState.Found:
        line_values: dict[str,str] = self.rgx_line.process_line(new_line_str)
        new_line_node: LogLineNode = LogLineNode( line_str= new_line_str, line_num=self.next_line_number )
        parse_test_result = new_line_node.populate_data( event_type_id=event_type_id, line_values=line_values )

#        self.module_types.add_node(new_line_node)
        self.file_context.write( f'{new_line_node}' )
        self.next_line_number += 1

        return parse_test_result

    def parse( self: Self ) -> None:
        self.file_context.parse_file()

    def finish( self: Self ) -> None:
        json_file: TextIO | None = None
        try:
            json_file = open( self.input_file_name + '.json', 'w', encoding='utf-8-sig' )
            with json_file:
                json_str: str = json.dumps(
                    self.modules, default=lambda o: o.__dict__, indent=4
                )
                json_file.write(json_str)

        except Exception as e:
            print( f'File "{self.input_file_name}": {e}' )

        finally:
            if json_file is not None:
                json_file.close()
