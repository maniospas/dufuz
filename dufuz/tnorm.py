import torch


def minimum(a, b):
    return torch.minimum(a, b)


def product(a, b):
    return a*b


def lukasiewicz(a, b):
    return torch.maximum(a+b-1, torch.tensor(0))


def hamacher(a, b):
    return a*b/(a+b-a*b)


def nilpotent(a, b):
    mins = torch.minimum(a, b)
    return torch.where(a+b > 1, mins, 0)
