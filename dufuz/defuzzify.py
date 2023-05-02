import torch


def plot(number):
    number.plot()


def cmean(number, threshold=1):
    if not hasattr(number, "values"):
        return number
    return float(torch.mean(torch.masked_select(number.domain.elements, number.values >= threshold-1.E-12)).cpu())


def mmean(number):
    if not hasattr(number, "values"):
        return number
    threshold = float(number.values.max().cpu())
    return float(torch.mean(torch.masked_select(number.domain.elements, number.values >= threshold)).cpu())


def wmean(number):
    if not hasattr(number, "values"):
        return number
    return float((torch.sum(number.values*number.domain.elements) / torch.sum(number.values)).cpu())
