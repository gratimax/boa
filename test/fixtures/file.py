# import string
# from ast import alias

a = b = 1 * 2 / 3 * (4 + 3) - 6 * 1.0e6

c = string


def annotation(str):
    def wrapped(fn):
        pass
        c = string
        print str

        '''~js
        // hooray, inlined js!
        console.log(str + 5);
        (function (x) {
            return x + 5;
        })(3);
        '''
        c.y(a)

        return fn
    return wrapped

@annotation('my_fn')
def my_fn(arg1, arg2):
    if arg1:
        for x in arg2:
            print x
        return arg1
    elif arg2:
        print arg2
    elif annotation():
        pass
    else:
        return None

def my_generator(arg1, arg2):
    #while True:
        #pass
        #yield 5
    return arg1 + arg2