class GraphMeta(type):

    @classmethod
    def __prepare__( mcls, name, bases, **kwds ):
        print(f'Prepare{mcls}:{name} with bases {bases} and kwds {kwds}' )
        return super().__prepare__(name, bases, **kwds)

    def __new__( mcls, name, bases, namespace, **kwds ):
        print(f'New called, {mcls}:{name} with bases {bases} with {namespace} and kwds {kwds}' )
        return super().__new__( mcls, name, bases, namespace, **kwds )

    def __init__(cls, name, bases, namespace, **kwds):
        print(f'Init called, {cls}:{name} with bases {bases} with {namespace} and kwds {kwds}')
        cls.new_attrib = 2
        super().__init__(name, bases, namespace)

class TestGraphMeta(metaclass=GraphMeta):
    attribute: int = 1

    def method( self ) -> int:
        return self.attribute

registry = {}

def register(cls):
        if cls.__name__ != "Parent":
            registry[cls.__name__] = cls

class ParentMeta(type):

    def __new__(cls, name, bases, attrs ):
        new_class = super(ParentMeta, cls).__new__(cls, name, bases, attrs )
        register(new_class)
        return new_class

class Child1(metaclass=ParentMeta):
    pass

class Child2(metaclass=ParentMeta):
    pass