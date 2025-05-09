from typing import Self

import sys
import threading as th
import multiprocessing as mp
import pyarrow as par

from loguru import logger

from sortedcontainers import SortedDict

from ..common import ModelPropTypes, LineRefList, ModelDictData
from ..arrow import ArrowResults, PropertyStats

class ModelProperty[ T: ModelPropTypes ]:
    def __init__( self: Self, name: str | None, alias: str | None, store_type: par.DataType, *kwargs ) -> None:
        super().__init__()

        #self.model:     ModelInfo | None = None
        self.ttype:     type = type(T)
        self.model_id:  str | None = None
        self.name:      str | None = name
        self.alias:     str | None = alias
        self.data: ModelDictData = kwargs if kwargs else ModelDictData()

        self.owner:     object | None = None

        self.store_type:  par.DataType = store_type

        self.import_queue: mp.Queue = mp.Queue()
        self.app_msgqueue: mp.Queue | None = None
        self.thread:      th.Thread | None = None

        self.status_triggercnt: int = self.data[ "status_triggercnt" ] if "status_triggercnt" in self.data else 5000

        self.keyvaluemap_to_refs: SortedDict[ T, LineRefList ] = SortedDict[T, LineRefList ]()
        self.valueindex_to_keyvalue: list[ T ] = []
        self.ref_to_keyvalue:        list[ T | None ] = []

        self.maxrownum:  int   = 0
        self.keycnt:     int   = 0
        self.refcnt:     int   = 0
        self.hitpct:     int   = 0
        self.isunique:   bool  = True
        self.use_dict:   bool  = False
        self.calc_stats: bool = True
        self.par_array: par.Array | None = None

    def get_thread( self: Self ) -> th.Thread:
        return self.thread

    def __set_name__( self: Self, owner: object, name: str ) -> None:
        self.name  = name
        self.owner = owner
        if "model" in self.owner.__dict__:
            model = self.owner.__dict__["model"]
            model.properties[ self.name ] = self
            self.model_id = model.model_id
        else:
            logger.error(f"{self.name} failure to attach to owner.__dict__['model']")

    def __get__( self: Self, instance: object, owner: object ) -> T | None:
        if self.name in instance.__dict__:
            return instance.__dict__[self.name]
        else:
            return None

    def __set__( self: Self, instance: object, value: T ) -> None:
        instance.__dict__[self.name] = value
        pass

    def start_import( self: Self, app_msgqueue: mp.Queue ) -> mp.Queue:
        self.app_msgqueue = app_msgqueue

        self.thread = th.Thread(
            target=self.main_loop,
            name=f"{self.name}-index",
            args = (self.import_queue,)
        )

        self.thread.start()
        return self.import_queue

    def main_loop( self: Self, queue: mp.Queue ) ->None:
        #self.app_msgqueue.put( keyindex_info )
        logger.info(f'[{self.name}-index]: Started' )
        outer_rownum: int = -999
        outer_value:  str = "empty"
        trace:  str = "init"
        try:
            while True:
                rownum, value = queue.get()
                outer_rownum = rownum
                outer_value  = value
                trace = "got queue"

                if rownum == -1:
                    trace = f"about to finalize - {len(value)} = {value}"
                    self.finalize(int(value))
                    trace = "done finalize"
                    break

                trace = f"about to call recv_value {rownum} {value} "
                self.recv_value( rownum, value )
                trace = "recv_value done"

                if rownum % self.status_triggercnt == 0:
                    #keyindex_info: keyIndexInfo = self.get_index_info()
                    #self.app_msgqueue.put( keyindex_info )
                    pass

        except ValueError as valexc:
            logger.error(f'({self.name}: {self.alias}) ValueError: {valexc}  {trace}  {outer_rownum} {outer_value}' )

        except Exception as exc:
            logger.error(f'({self.name}: {self.alias}) Exception: {exc}  {trace}' )

        logger.info(f"({self.name}: {self.alias}) maxrow: {self.maxrownum} key2ref: {len(self.keyvaluemap_to_refs)} refs: {self.refcnt}")

    def recv_value( self: Self, row_num: int, import_value: T ) -> None:
        #self.counts[ import_value.name ] += 1
        self.maxrownum = max( self.maxrownum, row_num )

        if import_value not in self.keyvaluemap_to_refs:
            self.keycnt += 1
            self.keyvaluemap_to_refs[ import_value ] = LineRefList()
        else:
            self.isunique = False

        self.keyvaluemap_to_refs[ import_value ].append( row_num )
        self.refcnt += 1

    def finalize( self: Self, maxrownum: int ) -> None:
        try:
            self.maxrownum = max( self.maxrownum, maxrownum )

            self.ref_to_keyvalue = [None] * ( self.maxrownum + 1 )
            #self.valueindex_to_keyvalue: list[T | None] = [ key for key, refs in self.keyvaluemap_to_refs.items() ]

            for key, reflist in self.keyvaluemap_to_refs.items():
                for ref in reflist:
                    if ref > self.maxrownum:
                        logger.error( f'({self.name}: {self.alias})  ref: {ref} > maxrownum: {self.maxrownum}' )
                    else:
                        self.ref_to_keyvalue[ ref ] = key

            ref2keysize = float( sys.getsizeof( self.ref_to_keyvalue) )
            valindexmapsize = float( sys.getsizeof(self.valueindex_to_keyvalue) + sys.getsizeof(self.keyvaluemap_to_refs) )
            comp_ratio = ( ref2keysize / valindexmapsize )

            self.hitpct    = round((self.refcnt / self.maxrownum) * 100)
            self.use_dict  = comp_ratio > 2.5
            self.par_array = par.array( self.ref_to_keyvalue, type=self.store_type )  # , self.store_type

            propstats = PropertyStats( self.name, self.alias, self.ttype.__name__, self.keycnt, self.refcnt, self.hitpct, self.isunique )
            ArrowResults.stash_results( self.model_id, self.name, self.par_array, propstats )

        except ValueError as valexc:
            logger.error(f'({self.name}: {self.alias}) ValueError: {valexc}' )

        except Exception as exc:
            logger.error(f'({self.name}: {self.alias}) Exception: {exc}' )

    def get_pararray(self: Self) -> par.Array | None:
        logger.info(f"({self.name}: {self.alias}) - {self.par_array} = {sys.getsizeof(self.par_array)}" )
        return self.par_array


