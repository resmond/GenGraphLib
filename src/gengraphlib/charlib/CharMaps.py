from collections import namedtuple
from enum import IntEnum

"""
---------------------------------------------------

add to Upper Asc        
6       Dollar       $      0x60
        Pct          %
        Amp          &
        Bang         !
        QMark        ?
        Tild         ~
        
Add to lower Asc        
        Degree       °          0xB0         
        WTick        `
        [ up to four more]  



        TAB
        LF
        NULL

6       At           @
        Splat        *
        Hash         #
        UScore       _
        
        Plus         +          0
        Minus        -          1
        Dot          .       0010
        Pipe         |          0

8       Colon        :       0000
        Eq           =          1
        Comma        ,       0011
        Semi         ;       0001
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

        
        
    Capital-Letters: 65(0x41) - 90(0x5A)
    Lower-Letters: 97(0x61) - 122(0x7A)
    Numeric: 48(0x30) - 57(0x39)
        
        
"""



