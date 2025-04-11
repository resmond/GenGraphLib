from typing import NamedTuple
from enum import IntEnum

from src.gengraphlib.charlib.CMask import int_to_cmask, cmask_to_str, CMaskDef

class CSeg( IntEnum ):
    LowerAscSeg  = 0b000   # 0b 000  - a-z + 6 Extra Char Defs
    UpperAscSeg  = 0b001   # 0b 001  - A-Z + 6 Extra Char Defs
    TokenSeg     = 0b010   # 0b 010  - 32 Tokens

    MarkerSeg    = 0b011   # 0b 011

    NumSegData   = 0b100   # 0b 1XX   - Hi-Bit + 7 bits of data
    NumSegPos    = 0b101   # 0b 10X   - for negative signed segment + 6 bits of data
    NumSegNeg    = 0b110   # 0b 11X   - for positive signed segment + 6 bits of data
    NumExpSeg    = 0b111   # 0b 111   - Hi-bit is final marker + 4 bits of exponent data (repeating)

def cseg_to_str( _cseg: CSeg ) -> str:
    match _cseg:
        case CSeg.LowerAscSeg:
            return "LowerAsc"
        case CSeg.UpperAscSeg:
            return "UpperAsc"
        case CSeg.TokenSeg:
            return "Token   "
        case CSeg.MarkerSeg:
            return "Marker  "
        case CSeg.NumSegData:
            return "NumData "
        case CSeg.NumSegPos:
            return "NumPos  "
        case CSeg.NumSegNeg:
            return "NumNeg  "
        case CSeg.NumExpSeg:
            return "NumExp  "
        case _:
            return "*Error-----"

class CCharDef( NamedTuple ):
    seg: CSeg
    val: int


char_cat_def = tuple[ CSeg, int]

def int_to_cchar( _cint: int ) -> char_cat_def:
    #_seg: CCatSeg = CCatSeg( _cint & 0xc0 >> 5 )
    #_val: int = _cint & 0x1f
    return CSeg( _cint & 0xc0 >> 5 ), _cint & 0x1f

def cchar_to_int( cchar_def: CCharDef ) -> int:
    return (cchar_def.seg << 5) | cchar_def.val

def cchar_to_str(_cint: int) -> str:
    match _cint:
        case 0:
            return "Null "
        case 8:
            return "BS   "
        case 9:
            return "Tab  "
        case 10:
            return "LF   "
        case 12:
            return "CR   "
        case 13:
            return "CR+LF"
        case 32:
            return "Sp   "
        case _:
            if _cint < 8:
                return f"{chr(_cint)}  "
            elif _cint in [11, 14, 15, 25, 28, 29, 30, 31]:
                return f"{chr(_cint)}   "
            elif _cint in [26, 27]:
                return f"{chr(_cint)}  "
            elif 15 < _cint < 25 or _cint in [173]:
                return f"{chr(_cint)}  "
            elif _cint < 127:
                return f"{chr(_cint)}    "
            elif _cint in [160]:
                return f"{chr(_cint)} "
            elif _cint < 160:
                return "     "
            else:
                return f"{chr(_cint)}    "

if __name__ == "__main__":

    test_str: str = "abcdefghijklmnopqrstuv"

    with open("/home/richard/data/jctl-logs/docs/cchar_map.txt", "w") as file:

        for cint in range( 0, 128 ):
            char: str = cchar_to_str( cint )

            chr_str: str = chr( cint )

            bbytes: bytes = bytes( str( cint ), 'utf-8' )
            bint: bytes = bytes( cint )

            bin_fstr = format( cint, '08b' )
            cchar_cat_slice = bin_fstr[ 0:3 ]
            cchar_val_slice = bin_fstr[ 3: ]

    #        seg: int = (cint & 0xc0) >> 6
            seg: int = (cint & 0xe0) >> 5
            val: int = (cint & 0x1f)

            cseg: CSeg = CSeg( seg )
            cseg_str: str = cseg_to_str( cseg )

            #[{cat}: {cat_oct}]   {val_oct} = {val:2} {cseg_str}

            cmask_def: CMaskDef = int_to_cmask( cint )


            cmask_mask_int: int = (cint & 0x70) >> 4

            cmask_mask_slice  = bin_fstr[ 1:4 ]
            cmask_val_slice  = bin_fstr[ 4: ]

            cmask_str = cmask_to_str( cmask_def.cmask )

            line = f"[{cint:3}: {cint:2X} ]:  {char}  {cint:8b}    cat: {cmask_mask_slice} [{cmask_mask_int:3b}] {cmask_def.cmask} - {cmask_str}      val: {cmask_val_slice}  {cmask_def.val:2} "
            print( line )
            file.write( line )
            file.write( "\n" )

        