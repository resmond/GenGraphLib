from typing import Self

#from .LogLines import  import LogLine
from ..graph.GraphNodeLib import GraphNodeBase, NodeDict
from .TextBootLogLines import TextBootLogLine

class TextLogModule( GraphNodeBase ):

    def __init__(self: Self, id: str) -> None:
        self.module_type_node: GraphNodeBase | None = None
        self.events: NodeDict[GraphNodeBase ] | None = None
        super().__init__( id=id )

    def add_event( self: Self, event_node: GraphNodeBase ) -> None:
        if self.events is None:
            self.events = NodeDict[GraphNodeBase]( id= "event_node_dict" )

        self.events[event_node.id] = event_node

class TextLogModules( NodeDict[ TextLogModule ] ):

    def __init__(self: Self, id: str = "module_node_dict") -> None:
        super().__init__( id=id )

    def __missing__(self, key) -> TextLogModule:
        self[key] = new_node = TextLogModule( id=key )
        return new_node

class TextLogModuleType( NodeDict[ TextLogModules ] ):

    def __init__( self: Self, id: str = "module_type_node" ) -> None:
        super().__init__( id=id )
        #self.module_nodes = ModuleNodeDict(id="model_node_dict")
        #self.module_nodes[line_node.module_id] = ModuleNode( id=line_node.module_id, module_type_node=self )

    def __missing__(self, key) -> TextLogModules:
        self[key] = new_node = TextLogModules( id=key )
        return new_node

class TextLogModuleTypes( NodeDict[ TextLogModuleType ] ):

    def __init__( self: Self ) -> None:
        super().__init__( id= "module_type_dict" )

    def __missing__(self, key) -> TextLogModuleType:
        self[key] = new_node = TextLogModuleType( id=key )
        return new_node

    def accept_line_node( self: Self, line_node: TextBootLogLine ) -> None:
        self[ line_node.module_type_id ][ line_node.module_id ] = line_node

    def __add__( self, other: TextBootLogLine ) -> None:
        self.accept_line_node(other)

#    def add_node( self: Self, line_node: ModuleTypeNode ) -> None:
#        self[ line_node.module_type_id ] = ModuleTypeNode(id=line_node.module_type_id, line_node=line_node)

    #def add_event( self: Self, event_node: UnmetConditionEvent ) -> None:
    #    self[ event_node.line_node.model_type_id ][ event_node.line_node.model_id] = event_node

    #def add_event_node( self, event_node: EventNode ) -> None:
    #    module_type_node: ModuleTypeNode = self[ event_node.line_node.module_type_id ]
    #    module_type_node[ event_node.line_node.module_type_id ] = module_node
    #    pass

