from __future__ import annotations

from typing import Self, Pattern, Match, overload
import regex as rx

TRX_GROUPPATTERN = tuple[str, str, str] | tuple[str, str] | str

class TRgxField:

    def __init__(self: Self, specifier: str, pre: str = "", tail: str = "") -> None:
        self.specifier: str = specifier
        self.pre: str = pre
        self.tail: str = tail

class XDict( dict[str, TRgxField] ):
    def __init__(self: Self) -> None:
        super(XDict, self).__init__()

class RgxField:

    @overload
    def __init__(self: Self, name: str, specifier: str, pre: str = "", tail: str = "") -> None:
        ...

    @overload
    def __init__( self: Self, name: str, trx_group: TRgxField ) -> None:
        ...

    @overload
    def __init__( self: Self, name: str, trx_groups: dict[str, TRgxField ] ) -> None:
        ...

    def __init__(
        self: Self,
        name: str,
        specifier_or_group: str | TRgxField | dict[str, TRgxField ],
        pre: str = "",
        tail: str = "",
    ) -> None:
        self.name = name
        if isinstance( specifier_or_group, TRgxField ):
            self.specifier = specifier_or_group.specifier
            self.pre = specifier_or_group.pre
            self.tail = specifier_or_group.tail
        else:
            self.specifier = specifier_or_group
            self.pre = pre
            self.tail = tail
        self._pattern: Pattern | None = None
        self._started: bool = False

    def __str__(self: Self) -> str:
        return f"{self.pre}(?P<{self.name}>{self.specifier}){self.tail}"

    def __repr__(self: Self) -> str:
        return f"{{'name:'{self.name}', ('{self.specifier}', '{self.pre}', {self.tail})}}"

    @property
    def rgx( self: Self ) -> str:
        return f"{self.pre}(?P<{self.name}>{self.specifier}){self.tail}"
"""
    RxLineDef
"""
class RgxLine:

    def __init__(self: Self, field_defs: dict[str, TRgxField ] | None= None) -> None:
        self.pattern: Pattern | None = None
        self.fields: dict[str, RgxField] = {}

        if field_defs:
            self.add_fields( field_defs )

    def add_field( self: Self, name: str, rgx_str: str ) -> None:
        self.fields[name] = RgxField( name, rgx_str )

    def add_fields( self: Self, field_defs: dict[str, TRgxField ] ) -> None:
        for name, rgx in field_defs.items():
            self.fields[name] = RgxField( name, rgx )

    def __add__( self: Self, other: RgxField ) -> Self:
        self.fields[other.name] = other
        return self

    def compile( self: Self ) -> bool:
        group_list_str: list[str] = []
        pattern_str: str = ""

        try:
            for thing in self.fields.values():
                group_list_str.append( thing.rgx )

            pattern_str = "".join( group_list_str )
            self.pattern = rx.compile( pattern_str )

        except Exception as e:
            print(f'RgxLine.compile: ({pattern_str}) {e}')

        return self.pattern is not None

    def process_line( self: Self, line: str ) -> dict[str,str]:
        results: dict[str,str] = {}

        if not self.pattern:
            self.compile()

        try:
            match: Match[str] | None = self.pattern.match(line)

            if match:
                results = match.groupdict()

        except Exception as e:
            print(f'PatternCtx.process_line: {e}')

        return results


