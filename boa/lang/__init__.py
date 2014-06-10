
def toPy(obj):
    # convert a JS object to a python one
    return obj

def toJS(obj):
    # convert a python object to a pure javascript one
    return obj

def asJS(*vars):
    # annotation on a function to say 'convert this to a JS object, please!'
    def wrapped(fn):
        return fn

    return wrapped


def asPy(*vars):
    # annotation on a function to say 'convert this to a python object, please!'
    def wrapped(fn):
        return fn

    return wrapped