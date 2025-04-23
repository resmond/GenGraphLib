from typing import Self

import sys
import pickle as pk

from dataclasses import dataclass



@dataclass
class TestCls:
    first_str: str
    second_str: str
    third_str: str
    first_int: int

    def to_tupple( self: Self ) -> tuple:
        return self.first_str, self.second_str, self.third_str

if __name__ == '__main__':
    test = TestCls("foo", "bar", "thing", 5 )
    tup = ("foo", "bar", "thing", 5 )
    print(f"test: {sys.getsizeof(test)}")
    print(f"tup:  {sys.getsizeof(tup)}")

    test_buf = pk.dumps(test)
    print(f"test_buf: {sys.getsizeof(test_buf)}")

    tup_buf = pk.dumps(tup)
    print(f"tup_buf: {sys.getsizeof(tup_buf)}")

    tests = (
        TestCls("foo", "bar", "thing", 5 ),
        TestCls("foo", "bar", "thing", 5 ),
        TestCls("foo", "bar", "thing", 5 ),
        TestCls("foo", "bar", "thing", 5 ),
        TestCls("foo", "bar", "thing", 5 ),
        TestCls("foo", "bar", "thing", 5 ),
        TestCls("foo", "bar", "thing", 5 ),
        TestCls("foo", "bar", "thing", 5 ),
        TestCls("foo", "bar", "thing", 5 ),
        TestCls("foo", "bar", "thing", 5 )
    )

    tups = (
        ("foo", "bar", "thing", 5 ),
        ("foo", "bar", "thing", 5 ),
        ("foo", "bar", "thing", 5 ),
        ("foo", "bar", "thing", 5 ),
        ("foo", "bar", "thing", 5 ),
        ("foo", "bar", "thing", 5 ),
        ("foo", "bar", "thing", 5 ),
        ("foo", "bar", "thing", 5 ),
        ("foo", "bar", "thing", 5 ),
        ("foo", "bar", "thing", 5 ),
    )

    tuplist = [
        ("foo", "bar", "thing", 5 ),
        ("foo", "bar", "thing", 5 ),
        ("foo", "bar", "thing", 5 ),
        ("foo", "bar", "thing", 5 ),
        ("foo", "bar", "thing", 5 ),
        ("foo", "bar", "thing", 5 ),
        ("foo", "bar", "thing", 5 ),
        ("foo", "bar", "thing", 5 ),
        ("foo", "bar", "thing", 5 ),
        ("foo", "bar", "thing", 5 )
    ]



    print(f"tests: {sys.getsizeof(tests)}")
    tests_buf = pk.dumps(tests)
    print(f"tests_buf: {sys.getsizeof(tests_buf)}")

    print(f"tups: {sys.getsizeof(tups)}")
    tups_buf = pk.dumps(tups)
    print(f"tups_buf: {sys.getsizeof(tups_buf)}")

    print(f"tuplist: {sys.getsizeof(tuplist)}")
    tuplist_bufs = pk.dumps(tuplist)
    print(f"tuplist_buf: {sys.getsizeof(tuplist_bufs)}")




"""
test: 48
tup:  72
test_buf: 147
tup_buf: 70
tests: 120
tests_buf: 384
tups: 120
tups_buf: 91
tuplist: 136
tuplist_buf: 92
"""