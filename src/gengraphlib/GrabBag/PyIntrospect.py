import sys
#import objgraph as obj

INDENT_SPACE = 4

def is_method_inherited(subclass, method_name):
    """Check if a method is inherited from a parent class."""
    for cls in subclass.mro():
        if method_name in cls.__dict__:
            return cls is not subclass
    return False

def print_methods(cls, base_classes, parent_methods, indent=0):
    spacing = ' ' * indent

    base_classes_str = ', '.join(base_classes)
    module = sys.modules[cls.__module__]
    file_path = getattr(module, '__file__',
                        'No file (built-in or interactive)')
    print(f"{spacing}Class: {cls.__name__} " +
          f"[{base_classes_str}]: {file_path}")

    for method_name in (m for m in dir(cls) if callable(getattr(cls, m))
                                               and not m.startswith("__")):
        is_overridden = method_name in parent_methods
        is_inherited = is_method_inherited(cls, method_name)
        if not is_inherited or not is_overridden:
            status = ""
            if is_overridden:
                status = " (Overridden)"
            elif is_inherited:
                status = " (Inherited)"
            print(f"{spacing}  - {method_name}{status}")
    print()

def inspect_hierarchy(cls, indent=0):
    # It's an instance, get its class
    if not isinstance(cls, type):
        print(f"Getting class name from instance: {cls.__class__}")
        cls = cls.__class__

    base_classes = {base.__name__ for base in cls.__bases__}
    parent_methods = {m for parent in cls.__bases__
                      for m in dir(parent)
                      if callable(getattr(parent, m))
                      and not m.startswith('__')}

    if cls.__bases__ == (object,):
        indent = 0
        print_methods(cls, base_classes, parent_methods, indent)
    else:
        for parent in cls.__bases__:
            indent = inspect_hierarchy(parent, indent)
        print_methods(cls, base_classes, parent_methods, indent)

    return indent + INDENT_SPACE


if __name__ == "__main__":
    #inspect_hierarchy(MyDerivedClass)
    pass
