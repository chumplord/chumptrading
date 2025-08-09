from collections import defaultdict
from functools import wraps
from time import perf_counter


def cache(func, key_func=None):
    mem = defaultdict(str)
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        key = (
               key_func(*args, **kwargs)
               if key_func is not None
               else hash(str(args) + str(kwargs))
              )
        if key not in mem.keys() or mem[key] is None:
            t0 = perf_counter()
            mem[key] = func(*args, **kwargs)
            t1 = perf_counter()
            if t1 - t0 > 1:
                print(f'[{func.__name__}] TOOK {t1-t0} seconds.')
        return mem[key]
    return wrapped_func
