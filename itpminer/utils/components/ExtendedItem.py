from itpminer.utils.components import ErrorChecker
from itpminer.utils.types import *


def create(time_rel: int, item) -> ExtendedItemType:
    ErrorChecker.check_type(time_rel, "time_rel", int)
    return (time_rel, item)


def check_type(extended_item: ExtendedItemType):
    ErrorChecker.check_type(extended_item, "extended_item", tuple)
    ErrorChecker.check_type(extended_item[0], "extended_time[0]", int)


def display(extended_item: ExtendedItemType) -> str:
    check_type(extended_item)
    return f"{extended_item[1]}({extended_item[0]})"
