from dufuz.core import Environment, Domain, Number
from dufuz.tnorm import lukasiewicz
import torch


class DiscreteEnvironment(Environment):
    def __init__(self,
                 device='cuda',
                 tnorm=lukasiewicz,
                 tol=0.01,
                 breadth=1,
                 lower=None,
                 upper=None,
                 strategy="modulo"):
        super().__init__(device=device, tnorm=tnorm)
        self.tol = tol
        self.breadth = breadth
        self.lower = lower
        self.upper = upper
        self.strategy = strategy

    def number(self, value, form=None, breadth=None):
        if breadth is None:
            breadth = self.breadth
        if isinstance(value, dict):
            assert form is None
            return Number(list(value.values()), Domain(list(value.keys()), self))
        if form is None:
            form = lambda x: abs(x)
        if isinstance(value, list):
            return [self.number(element, form) for element in value]
        # TODO: implement the following with torch
        ret = {value: 1}
        offset = 0
        prob = 1
        while offset+self.tol < breadth:
            offset += self.tol
            prob -= self.tol/breadth
            ret[value+offset] = form(prob)
            ret[value-offset] = form(prob)
        return Number(list(ret.values()), Domain(list(ret.keys()), self))

    def discretize(self, values, numbers):
        if numbers.dtype == torch.bool:
            return values, numbers
        values, numbers = super().discretize(values, numbers)
        numbers = numbers if hasattr(numbers, "numpy") else torch.tensor(numbers, device=self.device)
        if self.lower and self.upper and self.strategy == "modulo":
            # makes the number filed a closed finite set
            numbers = torch.where(numbers < self.upper, numbers, numbers+(-self.upper+self.lower))
            numbers = torch.where(numbers > self.lower, numbers, numbers+(-self.lower+self.upper))
        elif (self.lower or self.upper) and self.strategy == "clip":
            numbers = torch.clip(numbers, self.lower, self.upper)

        rounded_numbers = torch.floor(numbers/self.tol+0.5)*self.tol
        return values, rounded_numbers
