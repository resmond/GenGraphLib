from typing import Self

from src.gengraphlib.graph import KeyDefBase
from src.gengraphlib.graph.KeySchemaBase import KeySchemaBase

from src.gengraphlib import (
    DictOfLists,
    KeyValTypes,
    ChainFilterBase,
    ChainableResult,
    #CommandChainSource
)


class BootLogChainFilter( ChainFilterBase[BootLogChainResult] ):
    def __init__( self: Self, key_schema: KeySchemaBase ) -> None:
        super(BootLogChainFilter, self).__init__()
        self.key_schema: KeySchemaBase = key_schema
        self.none_values: DictOfLists = DictOfLists()
        self.missing_keys: list[str] = []

    async def _filter_result( self: Self, input_result: BootLogChainResult ) -> BootLogChainResult | None:
        if input_result is None:
            return self.null_result
        else:
            return input_result

    def process_keyvalue( self, key_def: KeyDefBase, value: KeyValTypes, rec_num: int, rec_line: str = "" ) -> bool:

        result: bool = False

        json_key = key_def.json_key

        if value is None:
            self.none_values.add_entry( json_key, rec_line )

        elif key_def.dologing:

            try:
                #do work here

                result = True
            except Exception as valexc:
                print( f"[KeyGraphBase.process_field ({json_key}:{json_key}={value})] type: {type( value )} ValueError: {valexc}" )

        else:
            if json_key not in self.missing_keys:
                self.missing_keys.append( json_key )

        return result

