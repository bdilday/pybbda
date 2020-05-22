# https://www.python.org/download/releases/2.2.3/descrintro/#__new__


class Singleton(object):
    """
    Base class to instantiate an object as a Singleton

    example usage,

    >>> class A(Singleton):
    ...     def __init__(self, x):
    ...         self.x = x
    >>> a1 = A(x=1)
    >>> a2 = A(x=2)
    >>> a1 is a2
    ... True


    """

    def __new__(cls, *args, **kwargs):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwargs)
        return it

    def init(self, *args, **kwargs):
        pass
