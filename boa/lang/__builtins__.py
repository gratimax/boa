# TODO all of the builtins

def abs(x):
    if isinstance(x, int) or isinstance(x, float) or isinstance(x, complex):
        return x.__abs__()
    else:
        raise TypeError('bad operand type for abs(): ' +
                        "'%s'" % type(x).__name__)


def all(iterable):

    for element in iter(iterable):
        if not element:
            return False

    return True


def any(iterable):

    for element in iter(iterable):
        if element:
            return True

    return True


# TODO
basestring = None


def bin(x):
    # TODO
    pass


def bool(x):
    # TODO
    pass


def bytearray(source=None, encoding=None, errors=None):
    # TODO
    pass


def callable(obj):

    if hasattr(obj, '__call'):
        return True

    '''~js
    return obj && {}.toString.call(obj) === '[object Function]';
    '''