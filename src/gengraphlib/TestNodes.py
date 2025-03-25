from typing import Self

from fileparse.GNodeLib import NodeBase, NodeDict

class TestNode(NodeBase):

    def __init__(self: Self, id:str, **kwargs) -> None:
        self.desc: str = "TestNode"
        super(TestNode, self).__init__(id=id, **kwargs)

class TestNodeDict( NodeDict[TestNode] ):

    def __init__(self: Self, id: str, **kwargs ):
        self.desc: str = "TestNodeDict"
        super(TestNodeDict, self).__init__(id=id, **kwargs)

    def __missing__(self, key) -> TestNode:
        self[ key ] = node = TestNode(key)
        return node

class TestClassifierNode(NodeDict[TestNodeDict]):

    def __init__(self: Self, id:str, **kwargs) -> None:
        self.desc: str = "TestClassifierNode"
        super(TestClassifierNode, self).__init__(id=id, **kwargs)

    def __missing__(self, key) -> TestNodeDict:
        self[ key ] = node = TestNodeDict( id=key )
        return node

def test():
    classifier = TestClassifierNode(id="test_classifier_node")
    class_1 = classifier["class-1"]

    first_node = classifier["class-1"][ "first" ]

    first_node.desc = "1"
    class_1["second"].desc = "2"
    class_1["third"].desc = "3"


    print(f'len: {len(classifier)}')
    print(f'len: {len(class_1)}')

    for key, node in classifier.items():
        print(f'classifer[ {key} ]: {node.desc}')

        for key2, node2 in node.items():
            print(f"classifer[ {key} ][ {key2} ]: {node.desc} {node2.desc}")

    print(classifier)

if __name__ == "__main__":
    test()

        