#------------------------------------------------------------------------
#  CMask
#------------------------------------------------------------------------
from enum import IntEnum
from typing import NamedTuple

class CMask( IntEnum ):
    Crud_0      = 0b000
    Crud_1      = 0b001
    Tokens      = 0b010
    Num         = 0b011

    UChar_0      = 0b100
    UChar_1      = 0b101
    LChar_0      = 0b110
    LChar_1      = 0b111

class CMaskDef( NamedTuple ):
    cmask: CMask
    val: int

def cmask_to_str( _cseg: CMask ) -> str:
    match _cseg:
        case CMask.Crud_0:
            return "Crud 0"
        case CMask.Crud_1:
            return "Crud 1"
        case CMask.Tokens:
            return "Tokens"
        case CMask.Num:
            return "Num   "
        case CMask.UChar_0:
            return "Upper 0"
        case CMask.UChar_1:
            return "Upper 1"
        case CMask.LChar_0:
            return "Lower 0"
        case CMask.LChar_1:
            return "Lower 1"
        case _:
            return "Err    "

def int_to_cmask( _cint: int ) -> CMaskDef:
    return CMaskDef( CMask( (_cint & 0x70) >> 4 ), _cint & 0x0F)

