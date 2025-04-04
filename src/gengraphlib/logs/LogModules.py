from typing import Self

#from .LogLines import  import LogLine
from src.gengraphlib import NodeBase, NodeDict, LogLine


class Module( NodeBase ):

    def __init__(self: Self, id: str) -> None:
        super( Module, self ).__init__( id=id )
        self.module_type_node: NodeBase | None = None
        self.events: NodeDict[NodeBase] | None = None

    def add_event( self: Self, event_node: NodeBase  ) -> None:
        if self.events is None:
            self.events = NodeDict[NodeBase]( id="event_node_dict" )
        self.events[event_node.id] = event_node

class Modules( NodeDict[ Module ] ):

    def __init__(self: Self, id: str = "module_node_dict") -> None:
        super( Modules, self ).__init__( id=id )

    def __missing__(self, key) -> Module:
        self[key] = new_node = Module( id=key )
        return new_node

class ModuleType( NodeDict[ Modules ] ):

    def __init__( self: Self, id: str = "module_type_node" ) -> None:
        super( ModuleType, self ).__init__( id=id )
        #self.module_nodes = ModuleNodeDict(id="model_node_dict")
        #self.module_nodes[line_node.module_id] = ModuleNode( id=line_node.module_id, module_type_node=self )

    def __missing__(self, key) -> Modules:
        self[key] = new_node = Modules( id=key )
        return new_node

class ModuleTypes( NodeDict[ ModuleType ] ):

    def __init__( self: Self ) -> None:
        super( ModuleTypes, self ).__init__( id= "module_type_dict" )

    def __missing__(self, key) -> ModuleType:
        self[key] = new_node = ModuleType( id=key )
        return new_node

    def accept_line_node( self: Self, line_node: LogLine ) -> None:
        self[ line_node.module_type_id ][ line_node.module_id ] = line_node

    def __add__( self, other: LogLine ) -> None:
        self.accept_line_node(other)

#    def add_node( self: Self, line_node: ModuleTypeNode ) -> None:
#        self[ line_node.module_type_id ] = ModuleTypeNode(id=line_node.module_type_id, line_node=line_node)

    #def add_event( self: Self, event_node: UnmetConditionEvent ) -> None:
    #    self[ event_node.line_node.model_type_id ][ event_node.line_node.model_id] = event_node

    #def add_event_node( self, event_node: EventNode ) -> None:
    #    module_type_node: ModuleTypeNode = self[ event_node.line_node.module_type_id ]
    #    module_type_node[ event_node.line_node.module_type_id ] = module_node
    #    pass

