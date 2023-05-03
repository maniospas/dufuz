from .interpreter import interpret
import torch
from . import DiscreteEnvironment, tnorm
import argparse


parser = argparse.ArgumentParser(description='Run a dufuz file.')
parser.add_argument("path", type=str)
parser.add_argument("--tol", type=float, default=0.01)
parser.add_argument("--device", type=str, default="cuda:0")
args = parser.parse_args()
env = DiscreteEnvironment(tnorm=tnorm.lukasiewicz, tol=args.tol, device=torch.device(args.device))
interpret(env, args.path)