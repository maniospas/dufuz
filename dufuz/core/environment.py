from dufuz.core import Number, Domain
import torch
import operator


def _unique(x, dim=0, sorted=False):
    # thanks to ehsansaleh here: https://github.com/pytorch/pytorch/issues/36748
    # adjusted to emulate the numpy sort
    unique, inverse, counts = torch.unique(x, dim=dim,
        sorted=sorted, return_inverse=True, return_counts=True)
    decimals = torch.arange(inverse.numel(), device=inverse.device) / inverse.numel()
    inv_sorted = (inverse+decimals).argsort()
    tot_counts = torch.cat((counts.new_zeros(1), counts.cumsum(dim=0)))[:-1]
    index = inv_sorted[tot_counts]
    return unique, index


class Environment:
    def __init__(self, device, tnorm=torch.minimum):
        self.device = device
        self.monitors = list()
        self.tnorm = tnorm

    def discretize(self, values, elements):
        #mask = torch.logical_not(torch.isnan(values))
        #return torch.masked_select(values, mask), torch.masked_select(elements, mask)
        return values, elements

    def apply(self, method, a, b=None):
        if not isinstance(a, Number):
            a = Number([1.], Domain([a], self))
        if b is not None and not isinstance(b, Number):
            b = Number([1.], Domain([b], self))
        if b is None:
            retvals = torch.reshape(a.values, shape=(1, -1))
            elements = method(torch.reshape(a.domain.elements, shape=(1, -1)))
        else:
            # compute combinations of a and b membership
            avals = torch.reshape(a.values, shape=(1, -1))
            bvals = torch.reshape(b.values, shape=(-1, 1))
            retvals = self.tnorm(avals, bvals)
            # compute combinations of method(a, b)
            elements = method(torch.reshape(a.domain.elements, shape=(1, -1)),
                              torch.reshape(b.domain.elements, shape=(-1, 1)))
        # squeeze
        values = torch.reshape(retvals, shape=[-1])
        elements = torch.reshape(elements, shape=[-1])
        # postprocess
        values, elements = self.discretize(values, elements)
        values, elements = self.reduce(values, elements)
        # find non-zero positions and gather respective values (memberships) and elements (method outputs)
        positions = (values != 0)# > 1.E-12)
        if positions.size() != values.size():
            values = torch.masked_select(values, positions)
            elements = torch.masked_select(elements, positions)
        for monitor in self.monitors:
            monitor.notify(elements.nelement(), None)
        return Number(values, Domain(elements, self))

    def reduce(self, values, elements):
        #values = torch.reshape(values, shape=[-1])
        #elements = torch.reshape(elements, shape=[-1])
        # keep only the largest values for each unique element (sort and then keep first occurences)
        sort_idx = torch.argsort(values, descending=True)
        values = values[sort_idx]
        elements = elements[sort_idx]
        elements, unique_idx = _unique(elements)
        values = values[unique_idx]
        return values, elements

    def point(self, value, membership=1):
        return Number([membership], Domain([value], self))

    def If(self, condition, a, b):
        # self.combine(condition * a, self.Not(condition) * b) is viable only for logical clauses
        if not isinstance(condition, Number):
            condition = Number([1], Domain([condition], self))
        if not isinstance(a, Number):
            a = Number([1], Domain([a], self))
        if not isinstance(b, Number):
            b = Number([1], Domain([b], self))
        ret = None
        for branch, membership in condition.todict().items():
            term = (a if branch == 1 else b)*Number([membership], Domain([1], self))
            if ret is None:
                ret = term
            else:
                ret = self.combine(ret, term)
        return ret

    def le(self, a, b):
        return self.apply(operator.le, a, b)#self.And(self.apply(operator.le, a, b), self.Not(self.apply(operator.gt, a, b)))

    def ge(self, a, b):
        return self.apply(operator.ge, a, b)#self.And(self.apply(operator.ge, a, b), self.Not(self.apply(operator.lt, a, b)))

    def lt(self, a, b):
        return self.apply(operator.lt, a, b)#self.And(self.apply(operator.lt, a, b), self.Not(self.apply(operator.ge, a, b)))

    def gt(self, a, b):
        return self.apply(operator.gt, a, b)#self.And(self.apply(operator.gt, a, b), self.Not(self.apply(operator.le, a, b)))

    def eq(self, a, b):
        return self.apply(operator.eq, a, b)#self.And(self.apply(operator.ge, a, b), self.apply(operator.le, a, b))

    def complement(self, a):
        return Number(1-a.values, a.domain)

    def Not(self, a):
        return 1-a #Number(a.values, Domain(1-a.domain.elements, a.domain.env))

    def And(self, a, b):
        return self.apply(operator.mul, a, b)

    def Or(self, a, b):
        return self.apply(lambda x, y: x + y - x * y, a, b)

    def combine(self, number1, number2):
        if number1 is None:
            return number2
        if number2 is None:
            return number1
        values = torch.concat([number1.values, number2.values])
        elements = torch.concat([number1.domain.elements, number2.domain.elements])
        values, elements = self.reduce(values, elements)
        return Number(values, Domain(elements, self))

    def getlist(self, values, item, default=None):
        if not isinstance(item, Number):
            item = Number([1], Domain([item], self))
        result = None
        for i, membership in item.todict().items():
            #if membership == 0:
            #    continue
            i = int(round(i))
            if i < 0 or i >= len(values):
                continue
            membership = Number([membership], Domain([1], self))
            result = self.combine(self.apply(operator.mul, values[i], membership), result)
        if result is None:
            if default is None:
                return None
            if not isinstance(default, Number):
                default = Number([1], Domain([default], self))
            return default
        return result
