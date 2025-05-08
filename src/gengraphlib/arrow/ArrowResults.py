from sortedcontainers import SortedDict
from typing import Self

import pyarrow as par
import pyarrow.parquet as parquet

from loguru import logger

class PropertyStats:
    def __init__( self: Self, name: str, alias: str, ttype: str, keycnt: int, refcnt: int, hitpct: int, unique: bool ) -> None:
        self.name: str = name
        self.alias: str = alias
        self.ttype: str = ttype
        self.keycnt: int = keycnt
        self.refcnt: int = refcnt
        self.hitpct: int = hitpct
        self.unique: bool = unique
        self.keys: SortedDict[str, int] = SortedDict[str,int]()

    def refhit( self, value: str ):
        if value not in self.keys:
            self.keys[ value ] = 0

        self.keys[ value ] += 1
        self.refcnt += 1
        self.unique = False

    def getstr( self: Self ) -> str:
        return f'{self.name}:{self.alias}[{self.ttype}] keycnt: {self.keycnt}  refcnt: {self.refcnt}  hitpct: {self.hitpct}  unique: {self.unique}'

ModelResults: type = dict[ str, par.Array     ]
StatsResults: type = dict[ str, PropertyStats ]

class ArrowResults:
    models: dict[ str, ModelResults ] = {}
    stats:  dict[ str, StatsResults ] = {}

    @classmethod
    def stash_results( cls, model_id: str, name: str, par_array: par.Array, propstats: PropertyStats | None = None ) -> None:
        if model_id not in ArrowResults.models:
            ArrowResults.models[ model_id ] = ModelResults()

        ArrowResults.models[ model_id ][ name ] = par_array

        if model_id not in ArrowResults.stats:
            ArrowResults.stats[ model_id ] = StatsResults()

        ArrowResults.stats[ model_id ][ name ] = propstats

    @classmethod
    def dump_stats( cls, filepath: str ):
        with open(f'{filepath}.stats',"w") as file:
            for model_id, modelstats in ArrowResults.stats.items():
                for name, propstats in modelstats.items():
                    logger.info(f'{model_id}:{name} - {propstats.getstr()}')
                    file.write(f'{model_id}:{name} - {propstats.getstr()}\n')

    @classmethod
    def write_arrowtable( cls, model_id: str, filepath: str ) -> None:
        try:
            model_results = ArrowResults.models[ model_id ]
            if model_results:
                column_names: list[str] = []
                arrow_arrays: list[par.Array] = []
                for name, array in model_results.items():
                    column_names.append( name )
                    arrow_arrays.append( array )

                arrow_table = par.table( arrow_arrays, column_names)
                parquet.write_table(table=arrow_table, where=filepath)
            else:
                logger.error(f'No model_resuls found in ArrowResults.models for [{model_id}]')

            ArrowResults.dump_stats(filepath)

        except KeyError as keyerr:
            logger.error(f"save_arrowtable( {filepath} ): Excption - {keyerr}")

        except Exception as ext:
            logger.error(f"save_arrowtable( {filepath} ): Excption - {ext}")

    @classmethod
    def get_modelresults( cls, model_id: str ) -> ModelResults | None:
        return ArrowResults.models[ model_id ]

