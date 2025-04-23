from typing import Self


class LogStats:
    def __init__(self: Self) -> None:
        self.key_stats: dict[str, int] = {}