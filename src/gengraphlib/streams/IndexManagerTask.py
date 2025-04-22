from typing import Self

import multiprocessing as mp

from .. import KeyValueSchema
from ..common import KeyValTypes
from ..graph.KeySchemaVisitor import KeySchemaVisitor
from ..graph.KeyDefs import StrKeyDef, IntKeyDef, BoolKeyDef, FloatKeyDef, TmstKeyDef
from ..graph.KeyValues import StrKeyValueSet, IntKeyValueSet, BoolKeyValueSet, FloatKeyValueSet, TmstKeyValueSet
from .IndexingTasks import (
    StrIndexingTask,
    IntIndexingTask,
    BoolIndexingTask,
    FloatIndexingTask,
    TmstIndexingTask,
)

from ..proc.TaskLib import IndexTaskInterface, IndexManagerInterface

class IndexManagerTask[ T: KeyValTypes ]( KeySchemaVisitor[None], IndexManagerInterface ):

    index_queuemap: dict[str, mp.Queue  ]          = dict[str, mp.Queue ]()
    index_taskmap:  dict[str, IndexTaskInterface ] = dict[str, IndexTaskInterface ]()

    def __init__( self: Self, keyvalue_schema: KeyValueSchema ) -> None:
        super( IndexManagerTask, self ).__init__()
        self.keyvalue_schema: KeyValueSchema = keyvalue_schema
        self.active_keys: set[str] | None = None
        self.state: str = "Init"

    def init_indexes( self: Self, active_keys: set[str] ) -> None:
        self.active_keys = active_keys
        self.keyvalue_schema.visit_schema(self)

    @staticmethod
    def register_index( index: IndexTaskInterface ) -> None:
        IndexManagerTask.index_queuemap[index.alias] = index.queue
        IndexManagerTask.index_taskmap[index.id()] = index

    @staticmethod
    def start_indexes() -> None:
        for index in IndexManagerTask.index_taskmap.values():
            index.start()

    @staticmethod
    def stop_indexes() -> None:
        for index in IndexManagerTask.index_taskmap.values():
            index.stop()

    def queues_byalias( self: Self ) -> dict[str, mp.Queue]:
        _queues_byalias: dict[str, mp.Queue] = dict[str, mp.Queue ]()

        for key, queue in IndexManagerTask.index_queuemap.items():
            _queues_byalias[key] = queue

        self.state = "bound to valve-pump"
        return _queues_byalias

    def visit_str( self: Self, keydef: StrKeyDef, keyvalues: StrKeyValueSet ) -> None:
        if keydef.key in self.active_keys:
            self.register_index( StrIndexingTask( keydef, keyvalues ) )

    def visit_int( self: Self, keydef: IntKeyDef, keyvalues: IntKeyValueSet ) -> None:
        if keydef.key in self.active_keys:
            self.register_index( IntIndexingTask( keydef, keyvalues ) )

    def visit_bool( self: Self, keydef: BoolKeyDef, keyvalues: BoolKeyValueSet ) -> None:
        if keydef.key in self.active_keys:
            self.register_index( BoolIndexingTask( keydef, keyvalues ) )

    def visit_float( self: Self, keydef: FloatKeyDef, keyvalues: FloatKeyValueSet ) -> None:
        if keydef.key in self.active_keys:
            self.register_index( FloatIndexingTask( keydef, keyvalues ) )

    def visit_tmst( self: Self, keydef: TmstKeyDef, keyvalues: TmstKeyValueSet ) -> None:
        if keydef.key in self.active_keys:
            self.register_index( TmstIndexingTask( keydef, keyvalues ) )

#-------------------------------------------------------------------



