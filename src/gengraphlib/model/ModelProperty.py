from typing import Self

import sys
import threading as th
import multiprocessing as mp

import pyarrow as par

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
            breakpoint()

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
        print(f'[{self.name}-index]: Started' )
        try:
            while True:
                rownum, value = queue.get()

                if rownum == -1:
                    self.finalize(int(value))
                    break

                self.recv_value( rownum, value )

                if rownum % self.status_triggercnt == 0:
                    #keyindex_info: keyIndexInfo = self.get_index_info()
                    #self.app_msgqueue.put( keyindex_info )
                    pass

        except ValueError as valexc:
            breakpoint()
            print(f'{type(self).__name__}({self.name}:{self.alias}) ValueError: {valexc}' )

        except Exception as exc:
            breakpoint()
            print(f'{type(self).__name__}({self.name}:{self.alias}) Exception: {exc}' )

        print(f"{type(self).__name__}({self.name}:{self.alias}) maxrow: {self.maxrownum} key2ref: {len(self.keyvaluemap_to_refs)} refs: {self.refcnt}")

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
            self.maxrownum = maxrownum

            self.ref_to_keyvalue = [None] * self.maxrownum
            #self.valueindex_to_keyvalue: list[T | None] = [ key for key, refs in self.keyvaluemap_to_refs.items() ]

            for key, reflist in self.keyvaluemap_to_refs.items():
                for ref in reflist:
                    self.ref_to_keyvalue[ ref ] = key


            ref2keysize = float( sys.getsizeof( self.ref_to_keyvalue) )
            valindexmapsize = float( sys.getsizeof(self.valueindex_to_keyvalue) + sys.getsizeof(self.keyvaluemap_to_refs) )
            comp_ratio = ( ref2keysize / valindexmapsize )

            self.hitpct    = round((self.refcnt / self.maxrownum) * 100)
            self.use_dict  = comp_ratio > 2.5
            self.par_array = par.array( self.ref_to_keyvalue, type=self.store_type )  # , self.store_type

            propstats = PropertyStats( self.name, self.alias, self.ttype.__name__, self.keycnt, self.refcnt, self.hitpct, self.isunique )
            ArrowResults.stash_results( self.model_id, self.name, self.par_array, propstats )

            # print(f'{type(self).__name__}({self.name}:{self.alias}) maxrow: {self.maxrownum} keys: {self.keycnt} refs: {self.refcnt} ratio: {comp_ratio} hitpct: {self.hitpct}' )
            # print(f"{type(self).__name__}({self.name}:{self.alias}) partype: {self.store_type} key2ref: {len(self.keyvaluemap_to_refs)} val2ref: {len(self.valueindex_to_keyvalue)} ref2key: {len(self.ref_to_keyvalue)}")
            # print(f"{type(self).__name__}({self.name}: par_array: {sys.getsizeof(self.par_array)}")

        except ValueError as valexc:
            print(f'{type(self).__name__}.finalize({self.name}:{self.alias}) ValueError: {valexc}' )
            breakpoint()

        except Exception as exc:
            print(f'{type(self).__name__}.finalize({self.name}:{self.alias}) Exception: {exc}' )
            breakpoint()

    def get_pararray(self: Self) -> par.Array | None:
        print(f"{type(self).__name__}({self.name}: get_pararray(): {self.par_array} = {sys.getsizeof(self.par_array)}" )
        return self.par_array


