from typing import Self

import multiprocessing as mp
import datetime as dt

from ..common import KeyValTypes
from ..graph.KeySchemaVisitor import KeySchemaVisitor
from ..graph.KeyDefs import StrKeyDef, IntKeyDef, BoolKeyDef, FloatKeyDef, TmstKeyDef
from ..graph.KeyValues import StrKeyValueSet, IntKeyValueSet, BoolKeyValueSet, FloatKeyValueSet, TmstKeyValueSet
from ..proc.TaskLib import TaskBase
from .IndexingTasks import (
    StrIndexingTask,
    IntIndexingTask,
    BoolIndexingTask,
    FloatIndexingTask,
    TmstIndexingTask,
)

from ..proc.TaskLib import IndexTaskInterface, IndexManagerInterface

class ValueIndexManagerTask[ T: KeyValTypes ]( TaskBase, KeySchemaVisitor[None], IndexManagerInterface ):
    indexes_by_key:   dict[str, IndexTaskInterface] = {}
    indexes_by_alias: dict[str, IndexTaskInterface] = {}

    very_beginning = dt.datetime.fromisoformat("1970-01-01")

    def __init__( self: Self ) -> None:
        super( ValueIndexManagerTask, self ).__init__( "value-pump" )
        self.data_msgqueue: mp.Queue | None = None

    def start( self: Self ) -> None:
        pass

    def main_loop( self: Self ) -> None:
        pass

    @staticmethod
    def register_index( index: IndexTaskInterface ) -> None:
        ValueIndexManagerTask.indexes_by_key[   index.keydef.key   ] = index
        ValueIndexManagerTask.indexes_by_alias[ index.keydef.alias ] = index

    @staticmethod
    def start_indexes() -> None:
        for index in ValueIndexManagerTask.indexes_by_key.values():
            index.start()

    @staticmethod
    def stop_indexes() -> None:
        for index in ValueIndexManagerTask.indexes_by_key.values():
            index.stop()

    def visit_str( self: Self, keydef: StrKeyDef, keyvalues: StrKeyValueSet ) -> None:
        self.register_index( StrIndexingTask( keydef, keyvalues ) )

    def visit_int( self: Self, keydef: IntKeyDef, keyvalues: IntKeyValueSet ) -> None:
        self.register_index( IntIndexingTask( keydef, keyvalues ) )

    def visit_bool( self: Self, keydef: BoolKeyDef, keyvalues: BoolKeyValueSet ) -> None:
        self.register_index( BoolIndexingTask( keydef, keyvalues ) )

    def visit_float( self: Self, keydef: FloatKeyDef, keyvalues: FloatKeyValueSet ) -> None:
        self.register_index( FloatIndexingTask( keydef, keyvalues ) )

    def visit_tmst( self: Self, keydef: TmstKeyDef, keyvalues: TmstKeyValueSet ) -> None:
        self.register_index(  TmstIndexingTask( keydef, keyvalues ) )

#-------------------------------------------------------------------



