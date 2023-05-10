# DUFuz
Incorporating discrete numeric fuzzy sets in Python algorithms.

**Dependencies**: `numpy`, `torch`, `matplotlib`, `ply`<br>
**Contact**: Manios Krasanakis (maniospas@hotmail.com)<br>
**License**: Apache 2


## :rocket: Quickstart
* [DUFuz Language Interpreter](docs/language.md)
* [Python Fuzzy Arithmetic API](docs/api.md)

The code below demonstrates a bubblesort algorithm that runs on
fuzzy inputs on the DUFuz interpreter.
A similar implementation can be written with the Python API.

```python
import random
from timeit import default_timer as time
import matplotlib.pyplot as plt

values = [1, 2, 4? or 3.5?1.5, 5?]  # 1 and 2 are not fuzzy
random.shuffle(values)

def bubblesort(values):
    for i in range(len(values)):
        for j in range(i+1, len(values)):
            vali = values[i]
            valj = values[j]
            comparison = vali < valj
            values[i] = vali if comparison else valj
            values[j] = valj if comparison else vali
            
start_time = time()
bubblesort(values)
print("Completed in", time()-start_time, "sec")

axs = plt.subplots(len(values), 1)[1]
for ax, val in zip(axs, values):
    val.plot(ax, True)
plt.show()
```
