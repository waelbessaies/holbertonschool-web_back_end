#!/usr/bin/env python3
"""
Complex types - functions
"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    multiplication
    """
    def function(var: float):
        """
        Complex types - functions
        """
        return var * multiplier
    return function
