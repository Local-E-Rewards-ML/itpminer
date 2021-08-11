from typing import Iterable, Optional, Dict
from itpminer.utils.components import ErrorChecker, DatList
from itpminer.utils.types import DatListType, PatternType


class Node():
    def __init__(self, dat_list: DatListType, parent: Optional["Node"] = None):
        if parent is not None:
            self.check_type(parent)
        self.parent = parent

        DatList.check_type(dat_list)
        self.value = dat_list

        self.children: Dict[PatternType, "Node"] = {}

    def check_type(self, node: Optional["Node"]):
        if node is not None:
            ErrorChecker.check_type(node, "Node", Node)

    def add_child(self, child: "Node"):
        self.check_type(child)
        self.children[child.value[0]] = child

    def add_children(self, children: Iterable["Node"]):
        isinstance(children, tuple)
        for child in children:
            self.check_type(child)
            self.add_child(child)

    def __repr__(self) -> str:
        return DatList.display(self.value) if self.value else str(None)
