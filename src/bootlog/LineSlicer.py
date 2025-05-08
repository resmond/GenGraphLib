from typing import Self, NamedTuple
from enum import IntEnum
from collections.abc import Generator

from loguru import logger

from ..gengraphlib import KeyValueTuple

class BCharType( IntEnum ):
    LowJunk    = -1      # [1:31]  with exceptions
    Special    =  1      # [0, 10, 12, 13] Null, Tab, Lf, Cr
    TokensA    =  2      # [32:47]
    Numric     =  3      # [48:57]  0-9
    TokensB    =  4      # [58:64]
    UChars     =  5      # [65:90]  A-Z
    TokensC    =  6      # [91:96]
    LChars     =  7      # [97:122] a-z
    TokensD    =  8      # [123:125]
    HighJunk   =  9      # [126:255]

class BinCharInfo( NamedTuple ):
    type:     BCharType
    cint:     int
    byte:     bytes
    cstr:     str
    junk:     bool
    char:     bool
    numeric:  bool
    upper:    bool
    token:    bool
    special:  bool
    linefeed: bool

    def infostr( self: Self ) -> str:
        info = list[str]()
        info.append( f'{self.type.name:8} - [{self.cint}-0x{self.byte:02x}-0b{self.bytes:08b}] - "{self.cstr}"' )
        info += "junk" if self.junk else None
        info += "char" if self.char else None
        info += "upper" if self.upper else "lower"
        info += "numeric" if self.numeric else None
        info += "token" if self.token else None
        info += "special" if self.special else None
        info += "linefeed" if self.linefeed else None
        return ' '.join(info)

class BChars( list[BinCharInfo] ):
    def __init__( self: Self ) -> None:
        super().__init__()

        self.hitcnts: list[int] = [0] * 256

        for cint in range(0,255):
            byte:      bytes = bytes(1)
            cstr:      str   = chr(cint)
            junk:      bool  = False
            numeric:   bool  = False
            char:      bool  = False
            upper:     bool  = False
            token:     bool  = False
            special:   bool  = False
            linefeed:  bool  = False
            bchr_type: BCharType

            if cint == 9:
                bchr_type = BCharType.Special
                special   = True
                token     = True
            elif cint == 10:
                bchr_type = BCharType.Special
                special   = True
                token     = True
                linefeed  = True
            elif cint == 12:
                bchr_type = BCharType.Special
                special   = True
                token     = True
            elif cint < 32:
                bchr_type = BCharType.LowJunk
                junk      = True
            elif cint < 48:
                bchr_type = BCharType.TokensA
                token     = True
            elif cint < 58:
                bchr_type = BCharType.Numric
                numeric   = True
            elif cint < 65:
                bchr_type = BCharType.TokensB
                token     = True
            elif cint < 91:
                bchr_type = BCharType.UChars
                char      = True
                upper     = True
            elif cint < 97:
                bchr_type = BCharType.TokensC
                token     = True
            elif cint < 123:
                bchr_type = BCharType.LChars
                char      = True
                upper     = False
            elif cint < 127:
                bchr_type = BCharType.TokensD
                token     = True
            else:
                bchr_type = BCharType.HighJunk
                junk      = True

            bchar = BinCharInfo(
                type = bchr_type,
                cint = cint,
                byte = byte,
                cstr = cstr,
                junk = junk,
                char = char,
                numeric = numeric,
                upper = upper,
                token = token,
                special = special,
                linefeed = linefeed
            )

            self.append(bchar)

    def getinfo( self: Self, cint: int ) -> BinCharInfo:
        if 0 <= cint < 256:
            self.hitcnts[cint] += 1
            return self[ cint ]
        else:
            logger.error("Invalid Character [0-255] - {cint}")
            raise KeyError( "Invalid Character [0-255] - {cint}" )

    def dump_hitcnts( self: Self ) -> None:
        for index, hits in enumerate(self.hitcnts):
            if hits > 0:
                char_info: BinCharInfo = self[index]
                logger.info( f'Hit Count: {hits:6} for {char_info.infostr()}' )

BytesArrayTuple: type = tuple[ int, bytes ]

class HitType(IntEnum):
    Equals = 37
    StartJunk = -1
    StartData = 0

JunkSpan: type = tuple[int,int]

class LineSlicer:
    def __init__( self: Self ) -> None:
        super().__init__()

        self.bchars = BChars()

        self.tail_buffer:     bytearray = bytearray()
        self.current_buffer:  bytearray | None = None
        self.buffer_len:      int  =  0
        self.line_start:      int  =  0
        self.equals_index:    int  = -1
        self.current_index:   int  = -1
        self.in_key:          bool = True
        self.is_junk:         bool = False

    def build_keyvalue( self: Self ) -> KeyValueTuple | None:
        try:
            keystr: str = self.current_buffer[self.line_start:self.equals_index].decode()
            valstr: str = self.current_buffer[self.equals_index+1:self.current_index].decode()
            #cur_span = bytearray(self.current_buffer[self.current_index - 3 : self.current_index + 3])

            #logger.info(f'key: {keystr} value: {valstr}')
            return keystr, valstr
        except Exception as exc:
            logger.error(f"decode error {exc}")
            return None

        # for junk_span in self.junk_spans:
        #     replacement_buf: bytes = b"$" * (junk_span[1] - junk_span[0] + 1)
        #     if junk_span[0] < self.equals_index:
        #         if len(self.junk_spans) == 1 and junk_span[0] == self.line_start:
        #             key_buffer = self.current_buffer[junk_span[1]:self.equals_index]
        #         else:
        #             key_buffer[junk_span[0]:junk_span[1]] = replacement_buf
        #     else:
        #         shifted_start: int = junk_span[0] - self.equals_index
        #         shifted_end:   int = junk_span[1] - self.equals_index
        #         val_buffer[shifted_start:shifted_end] = replacement_buf
        #

    def pass_buffer(self: Self, buffer: bytes ) -> Generator[tuple[str, str], None]:
        self.current_buffer = bytearray(self.tail_buffer + buffer)
        self.buffer_len     = len(self.current_buffer)
        self.tail_buffer    = bytes(0)
        self.current_index  = -1
        self.line_start     = 0


        while keyvalue_result := self._next_keyvalueline():
            if keyvalue_result[0] != 'skip':
                yield keyvalue_result

    def _next_keyvalueline( self: Self ) -> KeyValueTuple | None :
        try:
            self.line_start   = self.current_index + 1
            self.in_key       = True
            self.junk_spans   = []
            self.equals_index = -1
            self.junk_offset  = -1

            while True:
                self.current_index += 1
                if self.current_index >= self.buffer_len:
                    self.tail_buffer = bytearray( self.current_buffer[self.line_start:] )
                    return None   # do end of buffer

                cint: int = self.current_buffer[ self.current_index ]
                bchar_info: BinCharInfo = self.bchars.getinfo( cint )

                if cint == 61:
                    self.equals_index = self.current_index
                    self.in_key = False

                elif bchar_info.linefeed:

                    if self.is_junk:
                        self.is_junk = False
                        return "skip", ""

                    if self.in_key:

                        #look_back    = bytearray(self.current_buffer[self.line_start-20:self.current_index])
                        #cur_line     = bytearray(self.current_buffer[self.line_start:self.current_index+1])
                        #cur_span     = bytearray(self.current_buffer[self.current_index-5:self.current_index+5])
                        #look_forward = bytearray(self.current_buffer[self.current_index:self.current_index+20])

                        if self.current_buffer[ self.current_index-1 ] == 10:
                            return '', ''
                        else:
                            return 'skip', ''
                    else:
                        return self.build_keyvalue()

                if bchar_info.junk:
                    self.is_junk = True
                    
                # else:
                #     if bchar_info.junk:
                #         look_back   = bytearray(self.current_buffer[self.line_start-20:self.current_index])
                #         cur_line = bytearray(self.current_buffer[self.line_start:self.current_index+1])
                #         look_forward = bytearray(self.current_buffer[self.current_index:self.current_index+20])
                #
                #         while True:
                #             self.current_index += 1
                #             if self.current_index >= self.buffer_len:
                #                 return None  # do end of buffer
                #
                #             cint: int = self.current_buffer[self.current_index]
                #             bchar_info: BinCharInfo = self.bchars.getinfo(cint)
                #             if not bchar_info.linefeed:
                #                 continue
                #             else:
                #                 return '', ''
                    #
                    #     if not self.in_junk:
                    #         look_back   = bytearray(self.current_buffer[self.line_start-20:self.current_index])
                    #         cur_line = bytearray(self.current_buffer[self.line_start:self.current_index+1])
                    #         look_forward = bytearray(self.current_buffer[self.current_index:self.current_index+20])
                    #         self.junk_offset = self.current_index
                    #         self.in_junk = True
                    # else:
                    #     if self.in_junk:
                    #         self.junk_spans.append( (self.junk_offset, self.current_index) )
                    #         self.in_junk = False


                                #return self.build_keyvalue()
                                #self.junk_spans = []
                                #self.line_start = self.current_index


        except Exception as exc:
            logger.error( f'Exception = {exc}' )
            return None

    def get_tail( self: Self ) -> tuple[str,str] | None:
        if len(self.tail_buffer):
            key, value = self.next_buffer(self.tail_buffer)
            return key, value
        else:
            return None










