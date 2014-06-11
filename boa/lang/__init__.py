
def to_py(obj):
    # convert a JS object to a python one
    return obj


def to_js(obj):
    # convert a python object to a pure javascript one
    return obj


def as_js(*vars):
    # annotation on a function to say 'convert this to a JS object, please!'
    def wrapped(fn):
        return fn

    return wrapped


def as_py(*vars):
    # annotation on a function to say 'convert this to a python object, please!'
    def wrapped(fn):
        return fn

    return wrapped