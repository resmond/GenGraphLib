from typing import Self, Any

from typing import NamedTuple


class Parms(NamedTuple):
    id: str
    children: dict[str, Any]

class Defs:
    def __init__(self: Self, id: str, **kwargs ) -> None:
        self.data = { kwargs }

class Def:
    def __init__(self: Self, d: dict[str: Any], **kwargs ) -> None:
        self.d: dict[str,Any] = d
        self.data = { kwargs }


if __name__ == '__main__':

    defs: Defs(
        "foo",
        other=5,
        why="why not",
        shouldi=False,
        children=[
            Defs("foo",
                width=5,
                height=10),
            Defs( id="bar",width=10, children=
                    {
                      "child1": Defs( "child1" ),
                    })
                ]
        )
