from dataclasses import dataclass, field
from typing import Self

from . import KeyValInfo

class CodePattern[ T ]:
    def __init__( self: Self, _info: T, pattern: str, isline: bool = True  ):
        super().__init__()

        self.info: T = _info
        self.pattern: str = pattern
        self.isline: bool = isline

    @property
    def render( self: Self ) -> str:
        if self.isline:
            return f"{self.pattern}\n"
        else:
            return f"{self.pattern}"

class InfoPattern( CodePattern[KeyValInfo ] ):
    def __init__( self: Self, _info: KeyValInfo, pattern: str ):
        super().__init__( _info, pattern )

@dataclass
class ImportsInfo:
    module: str
    as_term: str | None = None
    objlist: list[str ] | None = None

class ImportPattern( CodePattern[ImportsInfo ] ):
    def __init__(self: Self, _info: ImportsInfo, pattern: str | None = None ):
        super().__init__(_info, pattern)
        self.info: ImportsInfo = _info
        self.pattern: str = pattern
        if _info.as_term is not None:
            self.pattern = f"import {_info.module} as {_info.as_term}"
        else:
            self.pattern = f"from {_info.module} import ({", ".join( _info.objlist )}"

@dataclass
class ClsLineInfo:
    clsname: str
    genic_var: str | None = None
    basecls: str | None = None

class ClsLinePattern( CodePattern[ClsLineInfo ] ):
    def __init__( self: Self, _info: ClsLineInfo, pattern: str | None = None ):
        super().__init__( _info, pattern )
        self.info: ClsLineInfo = _info
        self.pattern = pattern
        if _info.basecls is None and _info.genic_var is None:
            self.pattern = "class {_info.clsname}:"
        elif _info.genic_var is None:
            self.pattern = f"class {_info.clsname}({_info.basecls}):"
        else:
            self.pattern = f"class {_info.clsname}[{_info.genic_var}]({_info.basecls}):"

@dataclass
class ParamInfo:
    name: str
    type: str | type

    @property
    def fcode( self: Self ) -> str:

        match self.type:
            case str():
                return f"{self.name}: {self.type}"
            case type():
                return f"{self.name}: {str(self.type)}"
            case _:
                return "error"

# def field() -> list[ParamInfo]:
#     return list[ParamInfo]()

@dataclass
class ClsFunctionInfo:
    fnname:      str
    return_type: str = 'None'
    params:      list[ParamInfo] = field(default_factory=list)
    hostcls:     str | None = None

class ClsFunctionPattern( CodePattern[ClsFunctionInfo] ):
    def __init__( self: Self, _info: ClsFunctionInfo, pattern: str | None = None ):
        super().__init__( _info, pattern )
        self.info: ClsFunctionInfo = _info
        self.pattern = "def {_info.fnname}() -> None:"

    def get_params( self: Self ):
        return ", ".join([ param.fcode for param in self.info.params ])

    def get_fpatterstr( self: Self, info: ClsFunctionInfo ) -> str:
        self.isline = False

        paramstr:   str = ", ".join([param.fcode for param in self.info.params])
        long_pattern: str = \
        f"def {info.fnname}( {paramstr} ) -> {self.info.return_type}:\
                                \
                                \
                                \
               return None      \
        "

        return long_pattern

    def get_patterstr( self: Self, info: ClsFunctionInfo ) -> str:
        paramstr:   str = ", ".join([ param.fcode for param in self.info.params ])

        long_pattern: tuple[str,...] = (
            f"def {info.fnname}( {paramstr} ) -> {self.info.return_type}:",
            "                             \
                return None"
        )

        # f"def {info.fnname}( {paramstr} ) -> {self.info.return_type}: \
        #                                                               \
        #                                                               \
        #                                                               \
        #        return None                                            \
        # ")

        return "\n".join(long_pattern)
