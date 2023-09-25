#!/usr/bin/env python3
"""
type an iterable object
"""
from typing import List, Iterable, Sequence, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Function return values with the appropriate types
    """
    return [(i, len(i)) for i in lst]
