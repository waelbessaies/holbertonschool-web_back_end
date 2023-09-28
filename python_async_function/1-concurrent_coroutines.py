#!/usr/bin/env python3
"""
module
"""
import asyncio
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """wait_random"""
    list_awaitables = []
    result_list = []

    for i in range(n):
        list_awaitables.append(asyncio.create_task(wait_random(max_delay)))

    for task in asyncio.as_completed(list_awaitables):
        result = await task
        result_list.append(result)

    return result_list
