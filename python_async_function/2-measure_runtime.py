#!/usr/bin/env python3
"""Measure the runtime"""
import asyncio
from timeit import default_timer as timer

wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """ returns total_time """
    start = timer()
    asyncio.run(wait_n(n, max_delay))
    end = timer()

    return (end - start) / n
