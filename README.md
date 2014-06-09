# boa
Please, don't mind the mess! There's still a lot of stuff to be done.

Boa is a JavaScript runtime for Python. 
This means that you can write Python, compile it to JavaScript, and run
your Python code within the browser. Sweet! This has applications for
game programming and writing web apps in full python.

## Modules

- __boa.gen__: a code generator, using python's ast module and then generating JS
- __boa.lang__: an implementation of a subset of Python's standard library, 
    along with some other utilities(mainly JS interop)
- __boa.dom__: a mapping of the JS dom apis to idomatic Python.
- __boa.game__: an implementation of some of the pygame libraries, so you can run your games in the browser
- __boa.tools__: tools for compiling, testing