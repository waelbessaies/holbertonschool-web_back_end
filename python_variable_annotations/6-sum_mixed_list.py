#!/usr/bin/env python3
"""
sum_mixed_list
"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """
    returns sum of list
    """
    total: int = 0
    for i in mxd_lst:
        total += i
    return total
