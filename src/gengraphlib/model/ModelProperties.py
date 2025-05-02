from typing import Self

from enum import StrEnum, IntEnum

import datetime as dt

from pyarrow import utf8, int64, date32, DataType, uint8, bool_

from .ModelPropertyBase import ModelPropertyBase

class StrModProp( ModelPropertyBase[str] ):
    def __init__(
        self: Self,
        mod_id: str | None = None,
        *,
        import_type: DataType = utf8(),
        store_type: DataType = uint8(),
        alias: str | None = None,
        use_dict: bool = False
    ) -> None:

        super().__init__( mod_id=mod_id, import_type=import_type, store_type=store_type, alias=alias, use_dict=use_dict )

class BranchModProp( ModelPropertyBase[str] ):
    def __init__(
        self: Self,
        mod_id: str | None = None,
        *,
        import_type: DataType = utf8(),
        store_type: DataType = uint8(),
        alias: str | None = None
    ) -> None:

        super().__init__( mod_id=mod_id, import_type=import_type, store_type=store_type, alias=alias, use_dict=True )

class IntModProp( ModelPropertyBase[int]):
    def __init__(
        self: Self,
        mod_id: str | None = None,
        *,
        import_type: DataType = int64(),
        store_type: DataType = uint8(),
        alias: str | None = None,
        use_dict: bool = False
    ) -> None:

        super().__init__( mod_id=mod_id, import_type=import_type, store_type=store_type, alias=alias, use_dict=use_dict )


class TmstModProp(ModelPropertyBase[dt.datetime]):
    def __init__( self: Self,
                  mod_id: str | None = None,
                  *,
                  alias: str | None = None,
                  import_type: DataType = int64(),
                  store_type:  DataType = date32(),
                  use_dict: bool = False
                  ) -> None:

        super().__init__( mod_id=mod_id, import_type=import_type, store_type=store_type, alias=alias, use_dict=use_dict )

class StrEnumModProp[T: StrEnum]( ModelPropertyBase[T] ):
    def __init__(
            self: Self,
            mod_id: str | None = None,
            *,
            alias: str | None = None,
            store_type:  DataType = uint8(),
        ) -> None:

        super().__init__( mod_id=mod_id, import_type=utf8(), store_type=store_type, alias=alias, use_dict=True )

class IntEnumModProp[T: IntEnum]( ModelPropertyBase[T] ):
    def __init__(
            self: Self,
            mod_id: str | None = None,
            *,
            store_type:  DataType = uint8(),
            alias: str | None = None,
        ) -> None:

        super().__init__( mod_id=mod_id, import_type=int64(), store_type=store_type, alias=alias, use_dict=True )

class BoolModProp( ModelPropertyBase[bool] ):
    def __init__(
            self: Self,
            mod_id: str | None = None,
            *,
            alias: str | None = None,
        ) -> None:

        super().__init__( mod_id =mod_id, import_type=int64(), store_type=bool_(), alias=alias )
