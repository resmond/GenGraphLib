import functools as fct

def sigleton(cls: type):
    cls._instance = None
    @fct.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if cls._instance is None:
            cls._instance = cls(*args, **kwargs)
        return cls._instance
    return wrapper_singleton

