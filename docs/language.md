# DUFuz interpreter

You can implement numeric fuzzy algorithms
in an interpreted language that has 
a high overlap with Python.

## Run a script

After installing the package via `pip install dufuz`
you can run a DUFuz script per: 
```cmd
python -m dufuz example_script.dfz --tol 0.01 --device gpu:0
```
where tolerance is the numerical tolerance of fuzzy 
numeric calculations.

## Language specification
The DUFuz language is planned to replicate the following Python
practices. Current features of the languages are marked:

- [x] crisp for loops
- [ ] fuzzy while loops
- [x] fuzzy inline if-else statement comprehension
- [ ] if-else statements with blocks of code 
- [x] fuzzy list element access 
- [x] numeric and logical operations
- [x] method definition
- [ ] argument defaults and keyword arguments 
- [ ] calling Python methods and class functions
- [ ] import of Python packages and methods
- [ ] fuzzy sets
- [ ] fuzzy dictionaries

The language naturally handles numeric fuzzy sets.
Triangular fuzzy numbers centered around `X` are
annotated as`X?Y`, where `?Y` indicates uncertainty
up to *+-Y* around the center (the triangle's base
is *2Y*). You can use `?` instead of `?1`. This lets
you define numeric fuzzy sets via the discrete
F-transform, for example as `5? or 6?2`.

You can use the `.plot()` method of the Python API
from within the DUFuz interpreter.



