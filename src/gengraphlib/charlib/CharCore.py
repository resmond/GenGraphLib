from typing import NamedTuple
from enum import IntEnum

"""
    cat_oct    = bin_chars[0:3]
    val (5bit) = bin_chars[3:]

    cat: int = (cint & 0xe0) >> 5
    val: int = (cint & 0x1f)

"""


class CSeg( IntEnum ):
    LowerAscSeg  = 0b000   # 0b 000  - a-z + 6 Extra Char Defs
    UpperAscSeg  = 0b001   # 0b 001  - A-Z + 6 Extra Char Defs
    TokenSeg     = 0b010   # 0b 010  - 32 Tokens

    MarkerSeg    = 0b011   # 0b 011

    NumSegData   = 0b100   # 0b 1XX   - Hi-Bit + 7 bits of data
    NumSegPos    = 0b101   # 0b 10X   - for negative signed segment + 6 bits of data
    NumSegNeg    = 0b110   # 0b 11X   - for positive signed segment + 6 bits of data
    NumExpSeg    = 0b111   # 0b 111   - Hi-bit is final marker + 4 bits of exponent data (repeating)




#char_cat_def = tuple[ CharCatagory, int]
CCharDef: NamedTuple[CSeg, int ] = NamedTuple[CSeg, int ]( "CCharDef")

def int_to_cchar( _cint: int ) -> CCharDef:
    #_seg: CCatSeg = CCatSeg( _cint & 0xc0 >> 5 )
    #_val: int = _cint & 0x1f
    return CSeg( _cint & 0xc0 >> 5 ), _cint & 0x1f

def cchar_to_int( cat_char: CCharDef ) -> int:
        return (cat_char.cat << 5) | cat_char.val

def cchar_to_str( _cint: int ) -> str:
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
            if _cint < 32:
                return f"{chr(_cint)}    "
            elif _cint < 128:
                return f"{chr(_cint)}    "
            elif _cint < 160:
                return "     "
            else:
                return f"{chr(_cint)}    "


if __name__ == "__main__":

    test_str: str = "abcdefghijklmnopqrstuv"

    for cint in range( 0, 256 ):
        char: str = cchar_to_str( cint )

        chr_str: str = chr( cint )

        b: bytes = bytes( str(cint), 'utf-8' )
        b_int: bytes = bytes( cint )

        bin_chars = format(cint, '08b')
        cat_oct = bin_chars[0:3]
        val_oct = bin_chars[3:]

#        seg: int = (cint & 0xc0) >> 6
        cat: int = (cint & 0xe0) >> 5
        val: int = (cint & 0x1f)

        with open("/home/richard/data/jctl-logs/docs/chmap.txt", "w") as file:
            line = f'{cint:3}: {char}  0x {cint:4X}| 0b {cint:08b} 2b {bin_chars} |{cat_oct}| [{cat}] |{val_oct}| [{val}]'
            print( line )
            file.write( line + "\n")

        