from functools import wraps
from typing import NamedTuple


class Register(NamedTuple):
    dictionary: dict

    def register(self, name, val=None):
        @wraps
        def decorator(f):
            def func(*args, **kwargs):
                self.dictionary[name] = val
                res = f(*args, **kwargs)
                return res

            return func

        return decorator
