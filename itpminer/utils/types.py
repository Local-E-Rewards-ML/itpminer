from typing import Dict, List, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from itpminer.utils.components.Node import Node

from typing import Any, Tuple

ExtendedItemType = Tuple[int, Any]
PatternType = Tuple[ExtendedItemType, ...]
DatListType = Tuple[PatternType, Tuple[int, ...]]


TreeDictType = Dict[PatternType, "Node"]
H2Type = Dict[PatternType, int]
FrequentPatternsType = List[PatternType]


@dataclass
class Rule:
    A: PatternType
    sup_A: float
    B: PatternType
    sup_B: float
    A_and_B: PatternType
    sup_A_and_B: float
    conf: float
    lift: float


@dataclass
class RuleDisplay:
    A: str
    sup_A: float
    B: str
    sup_B: float
    A_and_B: str
    sup_A_and_B: float
    conf: float
    lift: float


RulesDictType = Dict[PatternType, Rule]
RulesDisplayDictType = Dict[PatternType, RuleDisplay]
