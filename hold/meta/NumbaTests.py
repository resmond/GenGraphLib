from enum import IntEnum
from typing import Self, NamedTuple
from collections import namedtuple
from dataclasses import dataclass

import sys
import pickle as pk


class CType(IntEnum):
    CStr = 0
    CInt = 1
    CFloat = 2
    CDouble = 3
    CLong = 4
    CULong = 5
    CLongLong = 6
    CULongLong = 7
    CShort = 8
    CUShort = 9

class Keydef:

    def __init__( self: Self,
            _json_key: str,
            _log_key:  str,
            _key_type: int
        ):
        self.json_key: str = _json_key
        self.log_key:  str = _log_key
        self.key_type: int = _key_type

    def totuple( self: Self ) -> tuple:
        return self.json_key, self.log_key, self.key_type

    def show( self ):
        print("")
        print("Keydef")
        print(f'json_key[{sys.getsizeof(self.json_key)}] = {self.json_key}')
        print(f'log_key[{sys.getsizeof(self.log_key)}] = {self.log_key}')
        print(f'sizeof: {sys.getsizeof(self)}')
        dir(self)


@dataclass
class KeydefData:
    json_key: str
    log_key:  str
    key_type: int

    def totuple( self: Self ) -> tuple:
        return self.json_key, self.log_key, self.key_type

    def pickel( self ) -> bytes:
        buffer = pk.dumps( self )
        print(f'KeyDefData buffer sizeof: {sys.getsizeof( buffer )}')

        return buffer

    def show( self ):
        print("")
        print("KeydefSlot")
        print(f'json_key[{sys.getsizeof(self.json_key)}] = {self.json_key}')
        print(f'log_key[{sys.getsizeof(self.log_key)}] = {self.log_key}')
        print(f'sizeof: {sys.getsizeof(self)}')
        dir(self)

class KeydefTuple(NamedTuple):
    json_key: str
    log_key:  str
    key_type: int

    # def totuple( self: Self ) -> tuple:
    #     return self.json_key, self.log_key, self.key_type
    #
    # def pickel( self: Self ) -> bytes:
    #     buffer = pk.dumps( self )
    #     print(f'KeydefSlot buffer sizeof: {sys.getsizeof( buffer )}')
    #     return buffer
    #
    # def show( self: Self ):
    #     print("")
    #     print("KeydefTuple")
    #     print(f'json_key[{sys.getsizeof(self.json_key)}] = {self.json_key}')
    #     print(f'log_key[{sys.getsizeof(self.log_key)}] = {self.log_key}')
    #     print(f'sizeof: {sys.getsizeof(self)}')
    #     dir(self)

if __name__ == '__main__':

    msg_key = Keydef( "msg", "MESSAGE", CType.CStr )
    msg_key.show()

    msg_key_slot = KeydefData( "msg", "MESSAGE", CType.CStr )
    msg_key_slot.show()

    msg_key_tuple = KeydefTuple( "msg", "MESSAGE", 0  )
    #msg_key_tuple.show()

    print(msg_key_tuple.json_key)
    print(msg_key_tuple)
    msg_key_tuple.json_key = "foo"
    print(msg_key_tuple)
    print("")

    keydefs_tup_native = (
        Keydef("msg", "MESSAGE", CType.CStr),
        Keydef("pri", "PRIORITY", CType.CStr),
        Keydef("tmst", "_REALTIME_TIME_STAMP", CType.CStr),
        Keydef("msg", "MESSAGE", CType.CStr),
        Keydef("pri", "PRIORITY", CType.CStr),
        Keydef("tmst", "_REALTIME_TIME_STAMP", CType.CStr),
        Keydef("msg", "MESSAGE", CType.CStr),
        Keydef("pri", "PRIORITY", CType.CStr),
        Keydef("tmst", "_REALTIME_TIME_STAMP", CType.CStr),
        Keydef("msg", "MESSAGE", CType.CStr),
    )

    keydefs_tup_map = tuple( map( lambda x: x.totuple(), keydefs_tup_native ) )
    keydefs_tup_reinit = tuple( Keydef( *keydef ) for keydef in keydefs_tup_map )
    keydefs_tup_reinit_map = tuple( map( lambda x: x.totuple(), keydefs_tup_native ) )


    print()
    print('keydefs_tup_map: ')
    cnt = -1
    for keydef in keydefs_tup_map:
        cnt += 1
        print(f'keydef[{cnt}]: {keydef}')
    print()

    print(f'msg_key: {sys.getsizeof(msg_key)}')
    print(f'msg_key_slot: {sys.getsizeof(msg_key_slot)}')
    print(f'keydefs_tup_native: {sys.getsizeof( keydefs_tup_native )}' )
    print(f'keydefs_tup_map: {sys.getsizeof( keydefs_tup_map )}' )
    print(f'keydefs_tup_reinit: {sys.getsizeof( keydefs_tup_reinit )}' )




    kdefs_tup_buffer = pk.dumps( keydefs_tup_native )
    keydefs_tup_map_buffer = pk.dumps( keydefs_tup_map )
    keydefs_tup_reinit_buffer = pk.dumps(keydefs_tup_reinit)
    keydefs_tup_reinit_map_buffer = pk.dumps(keydefs_tup_reinit_map)

    print(f'kdefs_tup_native sizeof: {sys.getsizeof( kdefs_tup_buffer )}' )
    print(f'keydefs_tup_map sizeof: {sys.getsizeof( keydefs_tup_map_buffer )}' )
    print(f'keydefs_tup_reinit sizeof: {sys.getsizeof( keydefs_tup_reinit_buffer )}' )
    print(f'keydefs_tup_reinit_map sizeof: {sys.getsizeof( keydefs_tup_reinit_map_buffer )}' )
    

