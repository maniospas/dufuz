# Python Fuzzy Arithmetic API for DUFuz

1. [Purpose](#purpose)
2. [Example](#example)

## Purpose

The purpose of this API is to support base operations needed by
DUFuz. However, you can also use it to fastly compute fuzzy
arithmetics.

## Example

First create a discrete environment for spawning and executing operations 
on numeric fuzzy sets. Provide a GPU `torch` device to the environment
to parallelize execution. The device is utilized as one logical core.

```python
import torch
from dufuz import DiscreteEnvironment
from dufuz import tnorm

env = DiscreteEnvironment(tnorm=tnorm.lukasiewicz,
                          tol=0.01, breadth=1,
                          device=torch.device('cuda:0'))
```

You can write algorithms involving normal Python operations.
An if-then-else statements on a fuzzy `condition` 
takes the form 
`condition.choose(result if true, result if false)`
where results can be numeric fuzzy sets.
Fuzzy boolean operations override the `&,|,~` operations
in place of the logical `and, or, not` respectively.
The DUFuz interpreter provides a pure Pythonic representation
of these operations.

As a demonstration. the following code implements the 
bubblesort algorithm for a list of fuzzy numbers in native Python.

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
