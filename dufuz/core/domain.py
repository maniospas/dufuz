import torch
from dufuz.core.number import Number


class Domain:
    def __init__(self, elements, env):
        self._elements = elements
        self._pos = None
        self.elements = elements if hasattr(elements, "numpy") else torch.tensor(elements, device=env.device)
        self.env = env

    @property
    def pos(self):
        # make this a delayed operation, because it is only needed by Domain.set and may delay other Number constructors
        if self._pos is None:
            elements = self._elements
            del self._elements
            self._pos = {k: i for i, k in enumerate(elements.cpu().numpy() if hasattr(elements, "numpy") else elements)}
        return self._pos

    def size(self):
        return self.elements.size()

    def set(self, values):
        raise Exception("Domain.set should not be called. Use Environment.number() with a dictionary instead.")
        import numpy as np
        spread = np.zeros(shape=self.elements.shape)
        for k, v in values.items():
            spread[self.pos[k]] = v
        return Number(torch.tensor(spread, device=self.env.device), self)
