from rayuela.fsa.fsa import FSA
import pickle
from rayuela.base.semiring import Tropical, Real
from rayuela.fsa.state import PairState, State
from rayuela.base.symbol import Sym, ε
import numpy as np
from rayuela.fsa.pathsum import Pathsum, Strategy

pickles_path = "autograding_tests/pickles"
hw_path = pickles_path + "/hw2"

with open(f"{pickles_path}/fsas.pkl", 'rb') as f:
    fsas = pickle.load(f)


def test_viterbi_fwd():
    
    with open(f"{hw_path}/hw2_viterbi_fwd.pkl", 'rb') as f:
        α = pickle.load(f)
    
    # Viterbi needs acyclic fsa
    acyclic_fsas = [fsa for fsa in fsas if fsa.acyclic]
    for fsa, a in zip(acyclic_fsas, α):
        assert Pathsum(fsa).forward(Strategy.VITERBI) == a

def test_edge_marginals():
    
    with open(f"{hw_path}/hw2_marginals.pkl", 'rb') as f:
        marginals = pickle.load(f)
    
    # Viterbi needs acyclic fsa
    acyclic_fsas = [fsa for fsa in fsas if fsa.acyclic]
    for fsa, marginal in zip(acyclic_fsas, marginals):
        assert fsa.edge_marginals() == marginal