import json

from typing import Self, TextIO

from fileparse.RgxCore import RgxLine, TRgxField
from fileparse.ParseTriggers import ParseTriggers, LineParseResult
from src.gengraphlib.logs.LogLines import LogLine, LogLines
from src.gengraphlib.logs.LogModules import ModuleTypes

#LINE_CALLBACK = Callable[ str, bool ]

class TextLogFileContext:

    fields: dict[str, TRgxField ] = {
        "date_seg": TRgxField(r"^\w*\s\w*\s\w*:\w*:\w*", tail=" "),
        "machine": TRgxField(r"\w*\S*", tail=" "),
        "thread_id": TRgxField(r"\w*\[\w*\]", tail=": "),
        "module_id": TRgxField(r"\w*-\w*", tail="."),
        "module_type_id": TRgxField(r"\w*", tail=" - "),
        "message": TRgxField(r".*"),
    }

    def __init__( self: Self) -> None:
        self.parse_triggers: ParseTriggers = ParseTriggers()
        self.rgx_line: RgxLine = RgxLine( field_defs = TextLogFileContext.fields )
        self.writer: TextIO

    def parse_file( self: Self, input_file_name: str, line_fn: callable ) -> None:

        try:
            with open( self.output_file_name, 'w', encoding='utf-8-sig' ) as self.writer:

                reader: TextIO
                with open( input_file_name, newline = '', encoding = 'utf-8-sig' ) as reader:
                    for line_str in reader:
                        line_fn( line_str )

        except Exception as e:
            print( f'File "{input_file_name}": {e}' )

    def logwrite( self: Self, text: str ) -> None:
        self.writer.write( text )

class TextLogGraph:

    def __init__( self: Self, input_file_name: str, output_file_name: str ) -> None:

        self._input_file_name = input_file_name
        self._output_file_name = output_file_name
        self.next_line_number: int = 0
        self.lines: LogLines = LogLines()
        self.module_types: ModuleTypes = ModuleTypes()

        #self.event_types: EventTypes = EventTypes()
#        self.event_types["unmet"] = EventTypeBase( id= "unmet", match_phrase = "unmet condition" )
#        from graphparse import EventTypeDict


    def process_line( self: Self, new_line_str: str ) -> LineParseResult:
        parse_test_result: LineParseResult = self.parse_triggers.execute( input_str= new_line_str )
        self.next_line_number += 1
        return parse_test_result

    def process_event( self: Self, event_type_id: str, new_line_str: str ) -> LineParseResult:

#        if parse_test_result is not None and parse_test_result[ "state" ] == ResultState.Found:
        line_values: dict[str,str] = self.rgx_line.process_line( new_line_str )
        new_line_node: LogLine = LogLine( line_str= new_line_str, line_num=self.next_line_number )
        parse_test_result = new_line_node.parse_line( event_type_id=event_type_id, field_values =line_values )

#        self.module_types.add_node(new_line_node)
        self.file_context.logwrite( f'{new_line_node}' )

        return parse_test_result

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
