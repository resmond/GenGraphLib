from typing import TypeVar
from collections import namedtuple





point_tup = namedtuple( 'Point', 'x, y', defaults=(1,) )
point_tup.__annotations__ = {'x': int, 'y': int}

PointType: type = TypeVar('PointType', bound=point_tup )

def tupler(_p: PointType) -> PointType:
    p1: PointType = _p
    p2: PointType = ("foo", 5)
    #p1= p1._replace(x=3)
    print(type(p2[0]))
    return p1

if __name__ == '__main__':
    # noinspection PyTypeHints
    p5: PointType = (3, 4)

    help(p5)
    help(PointType)
    tupler(p5)

