from typing import Tuple
from itpminer.utils.components import ErrorChecker, Pattern
from itpminer.utils.types import *


def check_type(dat_list: DatListType):
    pattern, time_abs_tuple = dat_list
    Pattern.check_type(pattern)
    ErrorChecker.check_type(time_abs_tuple, "time_abs_tuple", tuple)
    for time_abs in time_abs_tuple:
        ErrorChecker.check_type(time_abs, "time_abs", int)


def create(pattern: PatternType, time_abs_tuple: Tuple[int, ...]) -> DatListType:
    check_type((pattern, time_abs_tuple))
    return (pattern, time_abs_tuple)


def display(dat_list: DatListType) -> str:
    check_type(dat_list)
    return f"{Pattern.display(dat_list[0])}<{', '.join(map(str, dat_list[1]))}>"
