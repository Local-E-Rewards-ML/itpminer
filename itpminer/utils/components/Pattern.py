from typing import Tuple
from itpminer.utils.components import ErrorChecker, ExtendedItem
from itpminer.utils.types import *


def check_type(pattern: PatternType):
    ErrorChecker.check_type(pattern, "pattern", tuple)
    for extended_item in pattern:
        ExtendedItem.check_type(extended_item)


def check_subset(subset: PatternType, superset: PatternType) -> bool:
    for s in [subset, superset]:
        check_type(s)
    return set(subset).issubset(superset)


def check_joinable(pattern1: PatternType, pattern2: PatternType) -> bool:
    for s in [pattern1, pattern2]:
        check_type(s)
    if len(pattern1) == len(pattern2):
        if len(pattern1) == 1:
            return True
        elif pattern1[:-1] == pattern2[:-1] and pattern1[-1] < pattern2[-1]:
            return True
    return False


def join(pattern1: PatternType, pattern2: PatternType) -> PatternType:
    for s in [pattern1, pattern2]:
        check_type(s)
    if not check_joinable(pattern1, pattern2):
        raise Exception(f"{pattern1} and {pattern2} are not joinable!")
    else:
        return (*pattern1, pattern2[-1])


def display(pattern: PatternType) -> str:
    check_type(pattern)
    return f"{{{', '.join([ExtendedItem.display(extended_item) for extended_item in pattern])}}}"
