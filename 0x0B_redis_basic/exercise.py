#!/usr/bin/env python3
""" Redis"""
import redis
import uuid
from functools import wraps
from typing import Callable, Union


def count_calls(method: Callable) -> Callable:
    """ decorator """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ wrap """
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """call history"""
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Wrapper function"""
        in_list_name = "{}:inputs".format(method.__qualname__)
        out_list_name = "{}:outputs".format(method.__qualname__)

        self._redis.rpush(in_list_name, str(args))
        output = method(self, *args, **kwds)
        self._redis.rpush(out_list_name, output)
        return output
    return wrapper


def replay(method: Callable):
    """ func """
    key = method.__qualname__
    input = key + ":inputs"
    output = key + ":outputs"
    redis = method.__self__._redis
    count = redis.get(key).decode("utf-8")
    print("{} was called {} times:".format(key, count))
    lstIn = redis.lrange(input, 0, -1)
    lstOut = redis.lrange(output, 0, -1)
    zip = list(zip(lstIn, lstOut))
    for k, v in zip:
        attr, data = k.decode("utf-8"), v.decode("utf-8")
        print("{}(*{}) -> {}".format(key, attr, data))


class Cache:
    """class cache"""

    def __init__(self):
        """ instance of the Redis"""
        self._redis = redis.Redis()
        self._redis.fulshdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generate a random key"""
        key = str(uuid.uuid1())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn=None) -> str:
        """get function"""
        if (self._redis.exists(key)):
            value = self._redis.get(key)
            if fn is None:
                return value

            return fn(value)
        return None

    def get_str(self, key: str) -> str:
        """get str"""
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """get_int"""
        return self.get(key, int)
