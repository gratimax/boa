a = b = 1 * 2 / 3 * (4 + 3) - 6 * 1.0e6

str()

def annotation(str):
    def wrapped(fn):
        print str
        return fn
    return wrapped

@annotation('myFn')
def myFn(arg1, arg2):
    if arg1:
        for x in arg2:
            print x
        return arg1
    elif arg2:
        print arg2
    else:
        return None