from itpminer.utils.types import *
import networkx as nx
import matplotlib.pyplot as plt


def rules_graph(rules_display_dict: RulesDisplayDictType, rules_dict: RulesDictType, weighted: bool = False, one_to_one: bool = False):
    rules_one_to_one_dict: RulesDictType = {}
    if one_to_one:
        for key, item in rules_dict.items():
            if len(item.A) == 1 and item.A[0][0] == item.B[0][0] == 0:
                rules_one_to_one_dict[key] = item

        rules_one_to_one_display_dict: RulesDisplayDictType = {}
        for key, item in rules_one_to_one_dict.items():
            rules_one_to_one_display_dict[key] = RuleDisplay(
                A=f"{item.A[0][1]}",
                sup_A=item.sup_A,
                B=f"{item.B[0][1]}",
                sup_B=item.sup_B,
                A_and_B=f"{item.A}&{item.B}",
                sup_A_and_B=item.sup_A_and_B,
                conf=item.conf,
                lift=item.lift
            )
        rules_display_dict = rules_one_to_one_display_dict

    plt.figure(figsize=(20, 10))
    G = nx.DiGraph()
    edge_labels = {}

    for rule in rules_display_dict.values():
        A_node = f"{rule.A}\nS:{round(rule.sup_A, 2)}"
        B_node = f"{rule.B}\nS:{round(rule.sup_B, 2)}"
        edge = (A_node, B_node)
        G.add_edge(*edge, weight=rule.lift)
        edge_labels[edge] = f"L: {round(rule.lift, 2)}, C: {round(rule.conf, 2)}"

    pos = nx.circular_layout(G)
    nx.draw(G, pos, node_size=5000, node_color='pink', alpha=0.9)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    if weighted:
        for edge in G.edges(data='weight'):
            nx.draw_networkx_edges(
                # There's a false positive test from mypy
                G, pos, edgelist=[edge], width=edge[2])  # type: ignore
    plt.show()