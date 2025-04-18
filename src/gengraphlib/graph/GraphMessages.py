from typing import Self

from .. import DataMsg, KeyValTypes


class IndexingProgressMsg(DataMsg):

    def __init__( self: Self, source_id: str, message: str | None = "", data: dict[str, str ] | None = None ) -> None:
        super(IndexingProgressMsg, self).__init__( source_id, message, data )

# class KeyValueValue:
#         def __init__(self, alias: str, value: bytes ) -> None:
#             self.alias: str   = alias
#             self.value: bytes = value

KeyValRec: type = tuple[str,bytes]

class RecordValuesMsg( DataMsg ):

    def __init__(self: Self, source_id: str ) -> None:
        super( RecordValuesMsg, self ).__init__( source_id, message=None, data_dict=None )
        self.source_id: str = source_id
        self.rec_num:   int = -1
        self.values:    list[KeyValRec] = []

    def add_value( self: Self, alias: str, value: bytes ) -> None:
        self.values.append( (alias, value ) )
        

class KeyValueMsg[T: KeyValTypes]( DataMsg ):

    def __init__(self: Self, source_id: str, rec_num: int, key: str,  value: T ) -> None:
        super( KeyValueMsg, self ).__init__( source_id, message=f"Key[{key}] = {value}", data_dict=None )
        self.source_id: str = source_id
        self.rec_num:   int = rec_num
        self.key:       str = key
        self.value:     T   = value


