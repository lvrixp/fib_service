'''A simple cache decorator
'''
class SimpleStrCache:
    def __init__(self, enable=True, limits=100*1024*1024):
        self.enable = enable
        self.limits = limits
        self.cache = {}
        self.length = 0

    def __call__(self, fun):
        self.fun = fun
        def call(*args):
            if not self.enable:
                return self.fun(*args)

            key = args
            result = self.cache.get(key)
            if result is None:
                result = self.fun(*args)
                if result is not None and self.length < self.limits:
                    self.cache[key] = result
                    self.length += len(result)
            return result
        return call

if __name__ == '__main__':

    from datetime import datetime
    import time

    @SimpleStrCache(enable=True, limits=10)
    def get_str(n):
        time.sleep(1)
        return '*'*n

    print get_str(3)
    print get_str(3)
    print get_str(3)
    print get_str(3)
    print get_str(8)
    print get_str(8)
    print get_str(8)
    print get_str(8)
    print get_str(11)
    print get_str(11)
    print get_str(11)
