from .interpreter import interpret
import torch
from . import DiscreteEnvironment, tnorm, negation
import argparse


parser = argparse.ArgumentParser(description='Run a dufuz file.')
parser.add_argument("path", type=str)
parser.add_argument("--tol", type=float, default=0.01)
parser.add_argument("--device", type=str, default="cuda:0")
parser.add_argument("--logic", type=str, default="lukasiewicz")
args = parser.parse_args()
env = DiscreteEnvironment(tnorm=getattr(tnorm, args.logic),
                          memory_logic_not=getattr(negation, args.logic),
                          tol=args.tol, device=torch.device(args.device))
interpret(env, args.path)