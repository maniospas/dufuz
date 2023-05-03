from dufuz.interpreter import interpret
import torch
from dufuz import DiscreteEnvironment, tnorm

env = DiscreteEnvironment(tnorm=tnorm.lukasiewicz, tol=0.01, device=torch.device('cuda:0'))
interpret(env, "test.dfz")
