from __future__ import annotations
from typing import Self, Protocol

import pyarrow as par
from sortedcontainers import SortedDict

from ..common import ModelPropTypes, LineRefList
from .ModelInfo import ModelInfo

class ModelProperty[ T: ModelPropTypes, ImportValueInterface ]:

    def __init__(
            self: Self,
            mod_id: str | None,
            import_type: par.DataType,
            store_type: par.DataType,
            alias: str | None,
            use_dict: bool = False
    ) -> None:

        super().__init__()

        self.model:     ModelInfo | None = None
        self.ttype:     type = type(T)
        self.mod_id:    str    | None = mod_id
        self.name:      str    | None = mod_id
        self.alias:     str    | None = alias
        self.owner:     object | None = None
        self.import_type: par.DataType = import_type
        self.store_type:  par.DataType = store_type
        self.use_dict: bool = use_dict
        self.counts: dict[str,int] = {}
        self.keymap: SortedDict[ T, LineRefList ] = SortedDict[str, LineRefList]()
        self.valueindex_to_keyvalue: list[ T ] = []
        self.ref_to_valueindex:      list[ int | None ] = []
        self.rownummax: float   = 1
        self.keycnt:    float   = 0
        self.refcnt:    float   = 0
        self.isunique:  bool    = True

    def __set_name__( self: Self, owner: object, name: str ) -> None:
        self.name  = name
        self.owner = owner

        if hasattr( self.owner, "model_info" ):
            self.model = self.owner.model_info
            if isinstance( self.model, ModelInfo ):
                self.model.register_properties()

    def __get__( self: Self, instance: object, owner: object ) -> T:
        return instance.__dict__[self.name]

    def __set__( self: Self, instance: object, value: T ) -> None:
        instance.__dict__[self.name] = value

    def recv_value( self: Self, row_num: int, import_value: T ) -> None:
        self.counts[import_value.name ] += 1
        self.rownummax = max(self.rownummax, row_num)

        if import_value not in self.keymap:
            self.keycnt += 1
            self.keymap[import_value] = LineRefList()
        else:
            self.isunique = False

        self.keymap[import_value].append(row_num)
        self.refcnt += 1

        return import_value.value

    def finalize( self: Self ) -> None:
        self.keycnt = len(self.keyvaluemap_to_refs)

        self.valueindex_to_keyvalue = [""] * self.keyvaluecnt
        self.ref_to_valueindex = [None] * self.maxrecnum

        valueindex: int = 0
        for key, reflist in self.keyvaluemap_to_refs.items():
            self.valueindex_to_keyvalue[valueindex] = key
            for ref in reflist:
                self.ref_to_valueindex[ref] = valueindex
            valueindex += 1

        comp_ratio = float(len(self.ref_to_valueindex)) / float(
            len(self.valueindex_to_keyvalue)
        )

        self.use_dict = comp_ratio > 2.5

    def get_pararray(self: Self) -> par.Array | None:
        key_index: list[T | None] = []
        for valueindex in self.ref_to_valueindex:
            if valueindex is not None:
                keyvalue = self.valueindex_to_keyvalue[valueindex]
                key_index.append(keyvalue)
            else:
                key_index.append(None)
        return par.array(key_index, type=par.utf8())

