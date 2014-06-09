class A:

    def __getattr__(self, key):
        def inside(a):
            return a + 3
        if key == '__call__':
            return inside
        elif key == 'abc':
            return 'def'
        else:
            return None

print A()(3)
