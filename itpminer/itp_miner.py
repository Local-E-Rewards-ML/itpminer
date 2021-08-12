# Imports
from collections import defaultdict
import pandas as pd
from typing import Dict, List
from itpminer.utils.components import Pattern
from itpminer.utils.components.Node import Node
from itpminer.utils.types import *


def join_2(alpha: PatternType, beta: PatternType, tree_dict: TreeDictType, H2: H2Type, min_freq: int, max_span: int):
    tree_dict = tree_dict.copy()
    for pattern in [alpha, beta]:
        Pattern.check_type(pattern)
        if len(pattern) != 1:
            raise Exception("Pattern is not of length 1")

    # candidate_datlist_dict has (key: pattern, value: dats)
    candidate_datlist_dict = defaultdict(set)

    alpha_extended_item = alpha[0]
    beta_extended_item = beta[0]
    for w in range(0, max_span):
        pattern_2 = (alpha_extended_item, (w, beta_extended_item[1]))
        if pattern_2 in H2:
            if H2[pattern_2] >= min_freq:
                alpha_dats = tree_dict[alpha].value[1]
                beta_dats = tree_dict[beta].value[1]

                for alpha_dat in alpha_dats:
                    if alpha_dat + w in beta_dats:
                        candidate_datlist_dict[pattern_2].add(alpha_dat)

    for candidate_pattern, candidate_dats_set in candidate_datlist_dict.items():
        if len(candidate_dats_set) >= min_freq:
            node = Node(parent=tree_dict[alpha], dat_list=(
                candidate_pattern, tuple(candidate_dats_set)))
            tree_dict[alpha].add_child(node)
            tree_dict[candidate_pattern] = node
    return tree_dict


def join_k(alpha: PatternType, beta: PatternType, tree_dict: TreeDictType, H2: H2Type, min_freq: int):
    tree_dict = tree_dict.copy()
    for pattern in [alpha, beta]:
        Pattern.check_type(pattern)

    time_alpha_last, item_alpha_last = alpha[-1]
    time_beta_last, item_beta_last = beta[-1]
    pair_of_last = ((0, item_alpha_last),
                    (time_beta_last-time_alpha_last, item_beta_last))
    if H2[pair_of_last] >= min_freq:
        theta_pattern = Pattern.join(alpha, beta)

        alpha_times = tree_dict[alpha].value[1]
        beta_times = tree_dict[beta].value[1]
        theta_times = tuple(set(alpha_times).intersection(set(beta_times)))
        if len(theta_times) >= min_freq:
            theta_dat_list = (theta_pattern, theta_times)
            node = Node(parent=tree_dict[alpha], dat_list=theta_dat_list)
            tree_dict[alpha].add_child(node)
            tree_dict[theta_pattern] = node

    return tree_dict


def DFS(alpha: PatternType, frequent_patterns: FrequentPatternsType, tree_dict: TreeDictType, H2, min_freq: int, max_span: int):
    tree_dict = tree_dict.copy()
    frequent_patterns.append(alpha)

    parent = tree_dict[alpha[:-1]]

    siblings_dict = parent.children
    siblings_patterns = sorted(list(siblings_dict.keys()))
    alpha_index = siblings_patterns.index(alpha)

    J_alpha = siblings_patterns[alpha_index+1:]
    for pattern in J_alpha:
        tree_dict = join_k(alpha, pattern, tree_dict, H2, min_freq)

    E_alpha = sorted(list(tree_dict[alpha].children.keys()))
    for pattern in E_alpha:
        tree_dict = DFS(pattern, frequent_patterns,
                        tree_dict, H2, min_freq, max_span)

    return tree_dict


FrequentPatternsListType = List[Tuple[PatternType, int]]
FrequentPatternsDictType = Dict[PatternType, int]


def itp_miner(database: List[List], min_sup: float = 0.5, max_span: int = 2) -> Tuple[TreeDictType, FrequentPatternsDictType, FrequentPatternsListType, pd.DataFrame]:
    """
    Main inter-transactional mining algorithm

    Parameters
    ----------
    database : List[List]
        Inter-transactional database which is a list of list of items(str/int)

    Optional Parameters
    ----------
    min_sup : float(default = 0.5)
        Minimim support value between 0 and 1 used for mining

    max_span: int(default = 2)
        Maximum number of time steps considered for inter-transactional patterns


    Returns
    -------
    tree_dict: Dict[PatternType, Node]
        A dictionary containing in which the key is the inter-transactional pattern and the corresponding value is the Node object from the tree graph between the patterns.
        The root node can be retrieved by the key of empty tuple: ``root_node = tree_dict[()]``

    frequent_patterns_dict: Dict[PatternType, int]
        A dictionary containing in which the key is the inter-transactional pattern and the corresponding value is the frequency from mining.

    frequent_patterns_list: List[PatternType]
        A simple list of frequent inter-transactional patterns above the minimum support.

    frequent_patterns_dataframe: pd.DataFrame
        A pandas dataframe with two columns: Inter-transactional pattern & Support

    Examples
    --------
    ::

        # Import itpminer and create a dummy database of inter transactions
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

        # Mine frequent inter-transactional patterns
        tree_dict, frequent_patterns_dict, frequent_patterns_list, frequent_patterns_dataframe = itp_miner(
            database=database)

        # Derive association rules from frequent patterns
        rules_dict, rules_display_dict, rules_dataframe = association_rules(
            tree_dict=tree_dict)
        print(rules_dataframe)

        # Plot a network graph between extended items
        rules_graph(rules_display_dict=rules_display_dict, rules_dict=rules_dict)

    """
    database = [sorted(list(set(itemset))) for itemset in database]
    min_freq: int = int(min_sup * len(database))

    # Key: pattern, Value: list of dats
    candidate_patterns = defaultdict(set)

    frequent_1_patterns: FrequentPatternsType = []
    root_node = Node(dat_list=((), tuple(range(len(database)))))
    tree_dict: TreeDictType = {(): root_node}
    H2: H2Type = defaultdict(int)

    for t, itemset in enumerate(database):
        for ind, item in enumerate(itemset):
            candidate_patterns[item].add(t)

            for item_next in database[t][ind+1:]:
                H2[((0, item), (0, item_next))] += 1

            for t_next in range(t+1, min(len(database), t+max_span)):
                for item_next in database[t_next]:
                    H2[((0, item), (t_next-t, item_next))] += 1

    for item, dats in candidate_patterns.items():
        if len(dats) >= min_freq:
            node = Node(parent=root_node, dat_list=(((0, item),), tuple(dats)))
            root_node.add_child(node)
            tree_dict[((0, item),)] = node
            frequent_1_patterns.append(((0, item),))

    frequent_patterns = frequent_1_patterns.copy()

    for alpha in frequent_1_patterns:
        J_alpha = frequent_1_patterns
        for pattern in J_alpha:
            tree_dict = join_2(alpha, pattern, tree_dict,
                               H2, min_freq, max_span)

        E_alpha = sorted(list(tree_dict[alpha].children.keys()))
        for pattern in E_alpha:
            tree_dict = DFS(pattern, frequent_patterns,
                            tree_dict, H2, min_freq, max_span)

    frequent_patterns_dict: FrequentPatternsDictType = {(): len(database)}
    for pattern in tree_dict:
        if pattern != ():
            frequent_patterns_dict[pattern] = len(tree_dict[pattern].value[1])

    frequent_patterns_list: FrequentPatternsListType = list(
        frequent_patterns_dict.items())

    frequent_patterns_df = pd.DataFrame(
        frequent_patterns_list, columns=["Pattern", "Support"])
    frequent_patterns_df["Support"] = frequent_patterns_df["Support"] / \
        len(database)

    return tree_dict, frequent_patterns_dict, frequent_patterns_list, frequent_patterns_df
