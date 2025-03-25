from traceback import format_exception_only

from typing import Self

from fileparse.GNodeLib import NodeBase, NodeDict
from graphparse import RgxLine, ParseTestResult, ResultState

class LogLineNode( NodeBase ):

    def __init__(self: Self, line_str: str, line_num: int) -> None:
        super(LogLineNode, self).__init__(line_str = line_str, line_num = line_num)
        self.rgx_line: RgxLine = RgxLine()
        self.event_type_id: str = ""
        self.date_seg: str = ""
        self.machine: str = ""
        self.thread_id: str = ""
        self.module_type_id: str = ""
        self.module_id: str = ""
        self.message: str = ""
        self.values: dict[str, str] | None = None

    def populate_data( self: Self, event_type_id: str, line_values: dict[str, str]  ) -> ParseTestResult | None:
        self.event_type_id = event_type_id

        result_state: ResultState = ResultState.NoneFound
        try:
            self.date_seg = line_values["date_seg"]
            self.machine = line_values["machine"]
            self.thread_id = line_values["thread_id"]
            self.module_type_id = line_values["module_type_id"]
            self.module_id = line_values["module_id"]
            self.message = line_values["message"]

        except format_exception_only as e:
            print(f"error: {self.line_str}")
            print(f"dict: {line_values}" )
            print(f"Eception:{e}")
            result_state = ResultState.Exception

        return ParseTestResult(state=result_state, values=line_values)

class LineNodeIndex(NodeBase, list[LogLineNode]):

    def __init__( self: Self ) -> None:
        #self.log_file_graph: LogFileGraph
        self.cnt: int = 0
        super(LineNodeIndex, self).__init__(id="lineNodeIndex")

    def add_line( self: Self, line_str: str, line_num: int ) -> LogLineNode:
        new_line: LogLineNode =  LogLineNode( line_str=line_str, line_num=line_num )
        self.append( new_line )
        return new_line

class ModuleNode( NodeBase ):

    def __init__(self: Self, id: str) -> None:
        super(ModuleNode, self).__init__(id=id)
        self.module_type_node: NodeBase | None = None
        self.events: NodeDict[NodeBase] | None = None

    def add_event( self: Self, event_node: NodeBase  ) -> None:
        self.events.append(event_node)

class ModuleNodeDict( NodeDict[ModuleNode] ):

    def __init__(self: Self, id: str = "module_node_dict") -> None:
        super(ModuleNodeDict, self).__init__(id=id)

    def __missing__(self, key) -> ModuleNode:
        self[key] = new_node = ModuleNode(id=key)
        return new_node

class ModuleTypeNode( NodeDict[ModuleNodeDict] ):

    def __init__(self: Self, line_node: LogLineNode | None = None, id: str = "module_type_node") -> None:
        super(ModuleTypeNode, self).__init__(id=id)
        #self.module_nodes = ModuleNodeDict(id="model_node_dict")
        #self.module_nodes[line_node.module_id] = ModuleNode( id=line_node.module_id, module_type_node=self )

    def __missing__(self, key) -> ModuleNodeDict:
        self[key] = new_node = ModuleNodeDict(id=key)
        return new_node

class ModuleTypeDict( NodeDict[ModuleTypeNode] ):

    def __init__( self: Self ) -> None:
        super(ModuleTypeDict, self).__init__(id="module_type_dict")

    def __missing__(self, key) -> ModuleTypeNode:
        self[key] = new_node = ModuleTypeNode(id=key)
        return new_node

#    def add_node( self: Self, line_node: ModuleTypeNode ) -> None:
#        self[ line_node.module_type_id ] = ModuleTypeNode(id=line_node.module_type_id, line_node=line_node)

    #def add_event( self: Self, event_node: UnmetConditionEvent ) -> None:
    #    self[ event_node.line_node.model_type_id ][ event_node.line_node.model_id] = event_node

    #def add_event_node( self, event_node: EventNode ) -> None:
    #    module_type_node: ModuleTypeNode = self[ event_node.line_node.module_type_id ]
    #    module_type_node[ event_node.line_node.module_type_id ] = module_node
    #    pass

class ModuleTypeNodeDict( NodeDict[ ModuleTypeNode ] ):

    def __init__(self: Self, id: str = "module_type_node_dict") -> None:
        super(ModuleTypeNodeDict, self).__init__(id=id)

    def __missing__(self, key) -> ModuleTypeNode:
        self[key] = new_node = ModuleTypeNode(id=key)
        return new_node

    def add_node( self: Self, module_type_id: str, module_id: str ) -> None:
        self.module_nodes[module_type_id] = ModuleNode(id=module_id)


"""
    def create_new( self: Self, line_num: int, line_str: str) -> LogLineNode:
        self.line_num = line_num
        self.line_str = line_str
        return LogLineNode( line_num=self.line_num, line_str=self.line_str )
"""
