from typing import Self


class TableModel:

    def __init__( self: Self, mod_id: str | None = None ) -> None:
        super().__init__()

        self.mod_id: str | None = None


