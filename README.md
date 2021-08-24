# Inter-Transactional Patterns Miner(itpminer)

[![image](https://img.shields.io/pypi/v/itpminer.svg)](https://pypi.python.org/pypi/itpminer)
[![image](https://img.shields.io/conda/vn/conda-forge/itpminer.svg)](https://anaconda.org/conda-forge/itpminer)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Local-eRewards/itpminer/blob/main/demo.ipynb)
[![image](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Python implementation of ITPMiner algorithm**[[1]](#1)

-   Free software: MIT license

## Features

-   Mine frequent inter-transactional items
-   Generate association rules between inter-transactional items
-   Generate a network graph of association rules
-   Type definitions provided for [mypy](http://www.mypy-lang.org/) type checker

## Installation

PIP:

```
pip install itpminer
```

Conda:

```
conda install -c conda-forge itpminer
```

## Example

See also [demo.ipynb](demo.ipynb) or [Colab Notebook](https://colab.research.google.com/github/Local-eRewards/itpminer/blob/main/demo.ipynb). The code below is available on [demo.py](demo.py).

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
```

<p align="center">
<img src="https://raw.githubusercontent.com/Local-E-Rewards-ML/itpminer/main/images/frequent_patterns.png" alt="frequent_patterns_dataframe" width="300"/>
</p>

```python
# Derive association rules from frequent patterns
rules_dict, rules_display_dict, rules_dataframe = association_rules(
    tree_dict=tree_dict)
```

<p align="center">
<img src="https://raw.githubusercontent.com/Local-E-Rewards-ML/itpminer/main/images/association_rules.png" alt="rules_dataframe" width="800"/>
</p>

```python
# Plot a network graph between extended items
rules_graph(rules_display_dict=rules_display_dict, rules_dict=rules_dict)
```

<p align="center">
<img src="https://raw.githubusercontent.com/Local-E-Rewards-ML/itpminer/main/images/rules_graph.png" alt="rules_graph" width="800"/>
</p>

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
