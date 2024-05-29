#!/usr/bin/env python3
""" Redis exercise """
import requests
import redis
from functools import wraps
import time

# Setup Redis connection
cache = redis.StrictRedis(host='localhost', port=6379,
                          db=0, decode_responses=True)


def cache_page(expiration=10):
    """Decorator to cache page content and track access count."""
    def decorator(func):
        @wraps(func)
        def wrapper(url):
            cache_key = f"page:{url}"
            count_key = f"count:{url}"

            # Check if the URL content is cached
            cached_content = cache.get(cache_key)
            if cached_content:
                print(f"Cache hit for URL: {url}")
                return cached_content

            # If not cached, fetch the content
            print(f"Cache miss for URL: {url}")
            content = func(url)

            # Cache the content with an expiration time
            cache.setex(cache_key, expiration, content)

            # Increment the access count
            cache.incr(count_key)

            return content
        return wrapper
    return decorator


@cache_page(expiration=10)
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text
