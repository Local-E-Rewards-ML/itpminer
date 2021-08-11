from itpminer.utils.types import *
from itpminer.utils.components import Pattern
import pandas as pd


def association_rules(tree_dict: TreeDictType, min_conf=0.1, min_lift=1) -> Tuple[RulesDictType, RulesDisplayDictType, pd.DataFrame]:
    root_node = tree_dict[()]
    database_len = len(root_node.value[1])
    rules_dict: RulesDictType = {}
    rules_display_dict: RulesDisplayDictType = {}

    def support(node):
        return len(node.value[1]) / database_len

    def antecedent_traverse(node_antecedent: "Node" = root_node):
        for node_consequent in node_antecedent.children.values():
            if node_antecedent is not root_node:
                consequent_last_extended_item = node_consequent.value[0][-1]
                pattern_antecedent = node_antecedent.value[0]
                pattern_consequent = ((0, consequent_last_extended_item[1]),)

                support_antecedent_and_consequent = support(node_consequent)
                support_antecedent = support(node_antecedent)
                support_consequent = support(tree_dict[pattern_consequent])

                confidence = support_antecedent_and_consequent / support_antecedent
                if confidence >= min_conf:
                    lift = confidence / support_consequent
                    if lift >= min_lift:
                        rules_dict[node_consequent.value[0]] = Rule(
                            A=pattern_antecedent,
                            sup_A=support_antecedent,
                            B=(node_consequent.value[0][-1],),
                            sup_B=support_consequent,
                            A_and_B=node_consequent.value[0],
                            sup_A_and_B=support_antecedent_and_consequent,
                            conf=confidence,
                            lift=lift
                        )
                        rules_display_dict[node_consequent.value[0]] = RuleDisplay(
                            A=Pattern.display(pattern_antecedent),
                            sup_A=support_antecedent,
                            B=Pattern.display((node_consequent.value[0][-1],)),
                            sup_B=support_consequent,
                            A_and_B=Pattern.display(node_consequent.value[0]),
                            sup_A_and_B=support_antecedent_and_consequent,
                            conf=confidence,
                            lift=lift
                        )
            antecedent_traverse(node_consequent)

    antecedent_traverse()

    return rules_dict, rules_display_dict, pd.DataFrame(rules_display_dict.values())
