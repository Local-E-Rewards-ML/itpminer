# itpminer

[![image](https://img.shields.io/pypi/v/itpminer.svg)](https://pypi.python.org/pypi/itpminer)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Local-eRewards/itpminer/blob/main/demo.ipynb)
[![image](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Python implementation of ITPMiner algorithm**[[1]](#1)

-   Free software: MIT license
-   Documentation: https://chanyoungs.github.io/itpminer

## Features

-   TODO
    -   Write read-me.

## Example
See [Demo Notebook](demo.ipynb) to see the outputs as well.

```python
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

```
## Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [giswqs/pypackage](https://github.com/giswqs/pypackage) project template.

## References

<a id="1">[1]</a>
Anthony J.T. Lee, Chun-Sheng Wang,
An efficient algorithm for mining frequent inter-transaction patterns,
Information Sciences,
Volume 177, Issue 17,
2007,
Pages 3453-3476,
ISSN 0020-0255,
https://doi.org/10.1016/j.ins.2007.03.007.
(https://www.sciencedirect.com/science/article/pii/S002002550700151X)
Keywords: Association rules; Data mining; Inter-transaction patterns
