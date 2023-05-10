# DUFuz Language Interpreter

1. [Run a script](#run-a-script)
2. [Language specification](#language-specification)
3. [Fuzzy loops](#fuzzy-loops)

You can implement numeric fuzzy algorithms
in an interpreted language that has 
a high overlap with Python. This supports
natural integration of predicates
that can not be overriden by the Python API.
For example, the Python statement
`z = condition.choose(x, y)` where 
`condition` is a boolean fuzzy set and `x,y`
are numeric fuzzy sets is expressed
as `z = x if condition else y`.

## Run a script

After installing the package via `pip install dufuz`
you can run a DUFuz script per: 
```cmd
python -m dufuz example_script.dfz --tol 0.01 --device cuda:0
```
where tolerance is the numerical tolerance of fuzzy 
numeric calculations. Use pytorch to find valid devices
install on your machines.

:warning: For fast running time of fuzzy arithmetics,
ensure that *tol<sup> -2</sup>* is smaller
than then number of GPU cores. Running the interpreter
on CPUs can be very slow, but if you must do it
select some coarse tolerance, such as *0.1*.

## Language specification

The DUFuz language is planned to replicate the following Python
practices. Current features of the languages are marked:

- [x] crisp for loops
- [x] fuzzy while loops
- [x] fuzzy inline if-else statement comprehension
- [ ] if-else statements with blocks of code 
- [x] fuzzy list element access 
- [x] numeric and logical operations
- [x] method definition
- [ ] argument defaults
- [x] keyword arguments 
- [x] call Python methods and class functions
- [x] import Python packages and methods
- [ ] fuzzy sets
- [ ] fuzzy dictionaries

The language naturally handles numeric fuzzy sets.
Triangular fuzzy numbers centered around `X` are
annotated as`X?Y`, where `?Y` indicates uncertainty
up to *+-Y* around the center (the triangle's base
is *2Y*). You can use `?` instead of `?1`. This lets
you define numeric fuzzy sets via the discrete
F-transform, for example as `5? or 6?2`.

You can use the `.plot()` method that the underlying
Python API attaches to the fuzzy sets
the DUFuz interpreter works with. You can also
import other methods, such as defuzzifiers.
For example, you can add the following to your script:

```python
from dufuz.defuzzify import cmean

values = ... # a list of fuzzy values
for val in values:
    print(cmean(val))
```

## Fuzzy loops

You can write `while` loops the same way as regular Python.
If fuzzy conditions are checked, then the confidence of the 
outcomes is applied to the final assignment of each internal
variable. Each possible value at break points (the points at
which there is a possibility of stopping based on the fuzzy 
contdition) are aggregated via a DUFuz `or`.


```python
from dufuz.defuzzify import wmean

x = 0
y = 0
while x < 3.5?:  # x in {[0,1,2]: 0.5, [0,1,2,3]: 1, [0,1,2,3,4]: 0.5}
    y = y + x
    x = x + 1
(x-1).plot()
y.plot()
print(wmean(y))
```
