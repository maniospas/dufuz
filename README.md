# dufuz
Incorporating discrete numeric fuzzy sets in Python algorithms.
These sets are more general than fuzzy numbers.

**Dependencies**: `numpy`, `torch`, `matplotlib`<br>
**Contact**: Manios Krasanakis (maniospas@hotmail.com)<br>
**License**: Apache 2

## :rocket: Quickstart
First create a discrete environment for spawning and executing operations 
on numeric fuzzy sets. Provide a GPU `torch` device to the environment
to parallelize execution. The device is used as one logical core.

```python
import torch
from dufuz import DiscreteEnvironment
from dufuz import tnorm

env = DiscreteEnvironment(tnorm=tnorm.lukasiewicz,
                          tol=0.01, breadth=1,
                          device=torch.device('cuda:0'))
```

You can write algorithms involving normal Python operations.
If-then-else statements that involve fuzzy comparisons 
take the form 
`condition.choose(result if true, result if false)`
and fuzzy boolean arithmetics use the `&,|` operations.

As a demonstration. the following code implements the 
bubblesort algorithm for a list of fuzzy numbers.

```python
def bubblesort(values):
    for i in range(len(values)):
        for j in range(i+1, len(values)):
            vali = values[i]
            valj = values[j]
            comparison = vali < valj
            values[i] = comparison.choose(vali, valj)
            values[j] = comparison.choose(valj, vali)
```

The list can be defined to hold triangle fuzzy numbers per:
```python
values = list(range(8))
values = env.number(values)
bubblesort(values)
```

Finally, results can be defuzzified:
```python
from dufuz.defuzzify import wmean

print([wmean(val) for val in values])
# [0.0, 1.0, 2.7, 3.5, 3.5, 4.3, 6.0, 7.0]
```