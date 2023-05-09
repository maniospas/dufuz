import torch


def lukasiewicz(a, b=0):
    if b is None:
        return 1 - a
    return 1 - a + b


def minimum(a, b=0):
    return torch.where(a <= b, torch.ones(size=a.size(), device=a.device), torch.zeros(size=a.size(), device=a.device))


def product(a, b=None):
    ratio = torch.zeros(size=a.size(), device=a.device) if b is None else b/a
    if b is None:
        b = 0
    return torch.where(a <= b, torch.ones(size=a.size(), device=a.device), ratio)
