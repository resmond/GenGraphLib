from typing import Self, NamedTuple

import sys as sys

str_key_cnt: int = 0

class StrKey:
    __slots__ = ('name', 'value', 'instance', 'owner', 'slot_name', 'slot_index')

    str_key_cnt: int = 0

    def __init__(self: Self, slot_name: str ) -> None:
        self.slot_name = slot_name
        self.slot_index = -1
        StrKey.str_key_cnt += 1

    def __set_name__(self: Self, owner: type, name: str) -> None:
        self.name  = name
        self.owner = owner

        cnt: int = -1
        for slot_id in self.__slots__:
            cnt += 1
            if slot_id == self.slot_name:
                print(f'cnt: {cnt}   slot_id: {slot_id}  name: {name}')
                break
        self.slot_index = cnt

        print(f'SET_NAME: {StrKey.str_key_cnt}  owner: {owner}  name: {name}  slot_name: {self.slot_name}  slot_index: {self.slot_index}')

    def __get__(self: Self, instance: object, owner: type) -> str:
        self.instance = instance
        print(f'GET: instance: [{type(instance)}] {instance} owner: {owner}')
        return self.value

    def __set__(self: Self, instance: object, value: str) -> None:
        print (f'SET: instance: [{type(instance)}] {instance} value: {value}')
        self.value = value

    def do_something( self: Self, num: int ) -> str:
        print(self.__slots__)

        return "something"

class Slice:
    __slots__ = ('slot_a', 'slot_b', 'slot_c', 'slot_d')
    key_a = StrKey('slot_a')
    key_b = StrKey('slot_b')
    key_c = StrKey('slot_c')
    key_d = StrKey('slot_d')

class NTup(NamedTuple):
    tup_a: str
    tup_b: int
    tup_c: Slice

if __name__ == '__main__':

    slice_1 = ( Slice())

    sl_1_size = sys.getsizeof(slice_1)

    single_slice = Slice()
    single_slice_size = sys.getsizeof(single_slice)

    slice_2 = ( Slice(), Slice(), Slice() )

    sl_2_size = sys.getsizeof(slice_2)

    slice_3 = (
        Slice(),
        Slice(),
        Slice(),
        Slice(),
        Slice(),
        Slice(),
        Slice(),
        Slice(),
        Slice(),
        Slice()
    )

    sl_3_size = sys.getsizeof(slice_3)

    slice_list = [
        Slice(),
        Slice(),
        Slice(),
        Slice(),
        Slice(),
        Slice(),
        Slice(),
        Slice(),
        Slice(),
        Slice()
    ]

    sl_list_size = sys.getsizeof(slice_list)

    single_tuple = NTup( "single_tuple", 1, Slice() )

    print(f'single_tuple: {single_tuple}')
    
    print(f'dir: {dir(single_tuple.tup_b)}')

    sl_single_tuple_size = sys.getsizeof(single_tuple)

    print(f'size of single_slice: {single_slice_size}')
    print(f'size of slice_1: {sl_1_size}')
    print(f'size of slice_2: {sl_2_size}')
    print(f'size of slice_3: {sl_3_size}')
    print(f'size of slice_list: {sl_list_size}')
    print(f'size of single_tuple: {sl_single_tuple_size}')
    









