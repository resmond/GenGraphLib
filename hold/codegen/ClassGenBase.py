from io import TextIOWrapper
from typing import Self

from . import (
    ClsLinePattern,
    ClsLineInfo,
    InfoPattern,
    ImportsInfo,
    ImportPattern,
    KeyValInfo,
    CodePattern
)

class GenCodeRenderer:
    def __init__(self: Self, filepath: str ):
        super().__init__()

        self.filepath: str = filepath
        self.output_file: TextIOWrapper | None = None

    def __enter__( self: Self ) -> Self:
        self.output_file = open( self.filepath, "w" )
        return self

    def __exit__( self: Self, exc_type, exc_val, exc_tb ):
        self.output_file.close()
        self.output_file = None

    def __add__( self: Self, other: CodePattern | list[CodePattern] | str ):
        match other:
            case str():
                self.output_file.write( other )
            case CodePattern():
                self.output_file.write( other.render )
            case list():
                for pattern in other:
                    self.output_file.write( pattern.render )

class ClassGenBase:
    def __init__( self: Self, clsname: str, filepath: str, info_list: list[KeyValInfo ] ):
        super().__init__()

        self.filepath: str = filepath
        self.clsname: str = clsname
        self.info_list: list[KeyValInfo] = info_list
        self.imports: list[CodePattern] = []
        self.clsline: ClsLinePattern = ClsLinePattern( _info = ClsLineInfo( clsname ) )
        self.instances: list[CodePattern] = []
        self.fluent: GenCodeRenderer = GenCodeRenderer( filepath )

    def add_initdef( self: Self, info: KeyValInfo ):
        self.instances.append( InfoPattern( info, f"    self.{info.key}: {info.pytype} = _{info.key}" ) )

    def init_template( self: Self ) -> None:
        typing_import = ImportPattern( _info = ImportsInfo( module="typing", objlist=["Self"] ) )
        self.imports.append( typing_import )

        for xinfo in self.info_list:
            self.add_initdef(xinfo)

    def write( self: Self ) -> None:
        with open( self.filepath, "w" ) as codefile:
            text_segments: list[str] = [pattern.render for pattern in self.imports]
            full_str: str = "".join(text_segments)
            codefile.write( full_str )

    def splat( self: Self ) -> None:
        with self.fluent as thing:
            thing + [
                self.imports,
                "\n",
                self.clsline,
                "\tdef __init__( self: Self ):\n",
                self.instances
            ]

class TestGen:
    def __init__( self: Self ):
        self.classgen = ClassGenBase("TstClass", "/home/richard/data/TestCls.py", [] )
        pass

if __name__ == "__main__":
    # info = KeyValInfo( "msg", "MESSAGE", KeyType.KStr, "str", str )
    # patter = InfoPattern( info, f"    self.{info.json_key}: {info.pytype_str} = {info.json_key}" )
    # print(patter.pattern)
    # print(patter.render)

    pass