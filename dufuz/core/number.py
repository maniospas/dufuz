import torch
import operator


class Number:
    def __init__(self, values, domain):
        self.domain = domain
        self.values = values if hasattr(values, "numpy") else torch.tensor(values, device=domain.env.device)
        assert self.domain.size() == self.values.size()

    @property
    def env(self):
        return self.domain.env

    def prob(self):
        assert self.values.size() != 0
        return Number(self.values / self.values.sum(), self.domain)

    def conf(self, div=None):
        assert self.values.size() != 0
        if div is None:
            div = self.values.max()
        return Number(self.values / div, self.domain)

    def center(self, threshold=1):
        return torch.masked_select(self.domain.elements, (self.values > threshold-1.E-12)).cpu().numpy()

    def plot(self, plt=None, hold=False):
        if plt is None:
            from matplotlib import pyplot as plt
        plt.scatter(self.domain.elements.cpu().numpy(), self.values.cpu().numpy(), marker='.')
        if not hold:
            plt.show()

    def todict(self, threshold=0):
        return dict({k: v for k, v in zip(self.domain.elements.cpu().numpy(), self.values.cpu().numpy()) if v > threshold})

    def choose(self, a, b):
        return self.env.If(self, a, b)

    def __str__(self):
        return str(self.todict(-1))

    def __and__(self, other):
        return self.env.And(self, other)

    def __or__(self, other):
        return self.env.Or(self, other)

    def __invert__(self):
        return self.env.Not(self)

    def __add__(self, other):
        return self.env.apply(operator.add, self, other)

    def __radd__(self, other):
        return self.env.apply(operator.add, self, other)

    def __sub__(self, other):
        return self.env.apply(operator.sub, self, other)

    def __rsub__(self, other):
        return self.env.apply(operator.sub, other, self)

    def __mul__(self, other):
        return self.env.apply(operator.mul, self, other)

    def __rmul__(self, other):
        return self.env.apply(operator.mul, other, self)

    def __truediv__(self, other):
        return self.env.apply(operator.truediv, self, other)

    def __rtruediv__(self, other):
        return self.env.apply(operator.truediv, other, self)

    def __floordiv__(self, other):
        return self.env.apply(operator.floordiv, self, other)

    def __rfloordiv__(self, other):
        return self.env.apply(operator.floordiv, other, self)

    def __round__(self, n=None):
        return self.env.apply(round, self, n)

    def __int__(self):
        return self.env.apply(int, self)

    def __float__(self):
        return self.env.apply(float, self)

    def __abs__(self):
        return self.env.apply(abs, self)

    def __le__(self, other):
        return self.env.le(self, other)#raise Exception("Unsupported operation, use Environment.le instead")

    def __lt__(self, other):
        return self.env.lt(self, other)#raise Exception("Unsupported operation, use Environment.lt instead")

    def __ge__(self, other):
        return self.env.ge(self, other)#raise Exception("Unsupported operation, use Environment.ge instead")

    def __gt__(self, other):
        return self.env.gt(self, other)#raise Exception("Unsupported operation, use Environment.gt instead")

    def __eq__(self, other):
        return self.env.eq(self, other)#raise Exception("Unsupported operation, use Environment.eq instead")
