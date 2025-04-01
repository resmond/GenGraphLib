from collections import namedtuple

from enum import IntEnum

"""
Segmentation

    Capital-Letters: 65(0x41) - 90(0x5A)
    Lower-Letters: 97(0x61) - 122(0x7A)
    Numeric: 48(0x30) - 57(0x39)
    
    Tokens:
        Null - 0x00
        Cr - 
        Lf -
        Cr + Lf 
        
        BOG_[LR]_AllUpper + AsciiChar
        BOG_[LR]_AllLower + AsciiChar
        BOG_[LR]_FirstUpper + AsciiChar
        BOG_[LR]_SingleTokenChar + Token + AsciiChar
        BOG_[LR]_SingleTokenQFrame + 
            Token - 
                =
                :
            QFrame 
                ''
                ""        
        BOG_[LR]_OpenClose + 
            '[]'
            '()'
            '{}'
            '<>'

---------------------------------------------------        
        WTick        `  
        
 
        Pct          %        000
        Amp          &        001
        Tild         ~        010
        Bang         !        011
        Dollar       $        100
        Hash         #        101
        At           @        110
        QMark        ?        111
        

        Splat        *          0
        Eq           =          1
        
        Pipe         |          0
        UScore       _          1

        Plus         +          0
        Minus        -          1


8       Colon        :       0000
        Semi         ;       0001

        Dot          .       0010
        Comma        ,       0011
        
        Quote        '       0100
        DQuote       "       0101

        BSlash       \       0110
        FSlash       /       0111

8       LQBrack      {       1000
        RQBrack      }       1001
        
        LBracket     [       1010
        RBracket     ]       1011
        
        LParen       (       1100
        RParen       )       1101
        
        LThan        <       1110
        GThan        >       1111

        
        
        
        
"""


class CCat(IntEnum):
    AsciiBase   = 0       # Hex 0x0 << 5 = 0x0
    AsciiUpper = 1      # Hex 0x1 << 5 = 0x02  00
    Numeric = 2
    Token = 3
    HexOct = 4
    OrderedSeg = 5
    NumDefs = 6
    OtherD = 7

class CToken(IntEnum):



CharData: type = namedtuple("CharData", ['CCat', 'RVal'])

CharMapArray: [CharData] = \
    [
        ( CCat.AsciiUpper, 65)
        ( CCat.AsciiUpper, 65)          # 0 - Null
    ]

