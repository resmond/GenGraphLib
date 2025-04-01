from collections import namedtuple
from enum import IntEnum

"""
    cat_oct    = bin_chars[0:3]
    val (5bit) = bin_chars[3:]

    cat: int = (cint & 0xe0) >> 5
    val: int = (cint & 0x1f)

"""


class CharCatagory(IntEnum):
    LowerAscSeg  = 0   #  0b 000  - a-z + 6 Extra Char Defs
    UpperAscSeg  = 1   #  0b 001   # 1 - A-Z + 6 Extra Char Defs
    TokenSeg     = 2   #  0b 010   # 2 - 32 Tokens
    MarkerSeg    = 3

    NumSegData   = 4   #   0b 1XX   # 6 - Hi-Bit + 7 bits of data
    NumSegPos    = 5   #   0b 10X   # 5 - for negative signed segment + 6 bits of data
    NumSegNeg    = 6   #   0b 11X   # 7 - for positive signed segment + 6 bits of data
    NumExpSeg    = 7   #   0b 111   # 3 - Hi-bit is final marker + 4 bits of exponent data (repeating)




CharCat: type = namedtuple[CharCatagory, int]( "CharCat", ["cat", "val"])

def intToCatChar(_cint: int) -> CharCat:
    return CharCat((_cint & 0xe0) >> 5, (_cint & 0x1f))

def catCharToInt( cat_char: CharCat) -> int:
        return (cat_char.cat << 5) | cat_char.val

def catCharToStr(_cint: int) -> str:
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
        """
        octfld: str = CharTools.int_to_octfld( cint )
        octstr: str = CharTools.int_to_octstr( cint )
        hexstr: str = f'{hex(cint)}'
        binfld: str = CharTools.int_to_binfld( cint )
        binstr: str = CharTools.int_to_binstr( cint )
        """

        test: CharCat = ( CharCatagory.NumericChar, 6)
        test_cat = test.cat

        char: str = catCharToStr( cint )

        chr_str: str = chr( cint )

        b: bytes = bytes( str(cint), 'utf-8' )
        b_int: bytes = bytes( cint )

        bin_chars = format(cint, '08b')
        cat_oct = bin_chars[0:3]
        val_oct = bin_chars[3:]

#        seg: int = (cint & 0xc0) >> 6
        cat: int = (cint & 0xe0) >> 5
        val: int = (cint & 0x1f)

        print(f'{cint:3}: {char}  0x {cint:4X}| 0b {cint:08b} 2b {bin_chars} |{cat_oct}| [{cat}] |{val_oct}| [{val}]' )

        