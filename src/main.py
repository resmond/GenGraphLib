from typing import Self

from gengraphlib import LogGraph

class Main:

    def __init__(self):
        self.log_graph: LogGraph = LogGraph( "./data/journalctl-4.txt", "./data/journalctl-4-data.txt" )

    def do_parse( self: Self ) -> None:
        self.log_file_graph.parse()

        reader: TextIO
        with open( self.input_file_name, newline = '', encoding = 'utf-8-sig' ) as reader:
            for line_str in reader:
                line_fn( line_str )


if __name__ == "__main__":
    main: Main = Main()
    main.do_parse()
