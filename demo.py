from itpminer.utils import association_rules, rules_graph
from itpminer import itp_miner

database = [
    ["a", "b"],
    ["a", "c", "d"],
    ["a"],
    ["a", "b", "c", "d"],
    ["a", "b", "d"],
    ["a", "d"]
]

tree_dict, frequent_patterns_dict, frequent_patterns_list, frequent_patterns_dataframe = itp_miner(
    database=database)

rules_dict, rules_display_dict, rules_dataframe = association_rules(
    tree_dict=tree_dict)

print(rules_dataframe)

rules_graph(rules_display_dict=rules_display_dict, rules_dict=rules_dict)
