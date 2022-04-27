from rayuela.fsa.fsa import FSA
from rayuela.base.semiring import Boolean, Tropical, Real
from rayuela.fsa.state import MinimizeState, PairState, State, PowerState
from rayuela.base.symbol import Sym, ε
from rayuela.fsa.scc import SCC
from rayuela.fsa.pathsum import Pathsum, Strategy
import pickle
from rayuela.base.misc import compare_fsas, compare_charts
import numpy as np

pickles_path = "autograding_tests/pickles"
hw_path = pickles_path + "/hw5"

with open(f"{hw_path}/fsas.pkl", 'rb') as f:
    fsas = pickle.load(f)

def test_bellman_ford():
    with open(f"{hw_path}/bellmanford_bwd.pkl", 'rb') as f:
        𝜷s = pickle.load(f)

    for fsa, 𝜷 in zip(fsas, 𝜷s):

        computed_beta = fsa.backward(Strategy.BELLMANFORD)

        assert compare_charts(𝜷, computed_beta)

def test_johnson():
    with open(f"{hw_path}/johnson.pkl", 'rb') as f:
        Ws = pickle.load(f)

    for fsa, w in zip(fsas, Ws):

        W = Pathsum(fsa).johnson()

        assert compare_charts(w, W)

def test_minimization():
    pass

def test_minimization_example():
    fsa = FSA(R=Boolean)
    fsa.set_I(State("a"), w=Boolean(True))

    # arcs from state a
    fsa.add_arc(State("a"), 1, State("b"), w=Boolean(True))
    fsa.add_arc(State("a"), 2, State("c"), w=Boolean(True))

    # arcs from state b
    fsa.add_arc(State("b"), 2, State("d"), w=Boolean(True))
    fsa.add_arc(State("b"), 1, State("a"), w=Boolean(True))

    # arcs from state c
    fsa.add_arc(State("c"), 2, State("f"), w=Boolean(True))
    fsa.add_arc(State("c"), 1, State("e"), w=Boolean(True))

    # arcs from state d
    fsa.add_arc(State("d"), 2, State("f"), w=Boolean(True))
    fsa.add_arc(State("d"), 1, State("e"), w=Boolean(True))

    # arcs from state f
    fsa.add_arc(State("f"), 2, State("f"), w=Boolean(True))
    fsa.add_arc(State("f"), 1, State("f"), w=Boolean(True))

    # arcs from state e
    fsa.add_arc(State("e"), 1, State("e"), w=Boolean(True))
    fsa.add_arc(State("e"), 2, State("f"), w=Boolean(True))

    # add final states
    fsa.add_F(State("c"), w=Boolean(True))
    fsa.add_F(State("d"), w=Boolean(True))
    fsa.add_F(State("e"), w=Boolean(True))

    mfsa = fsa.minimize()

    MFSA = FSA(R=Boolean)
    MFSA.set_I(MinimizeState([State("b"), State("a")]), w=Boolean(True))
    MFSA.add_arc(MinimizeState([State("e"), State("c"), State("d")]), 2, MinimizeState([State("f")]), w=Boolean(True))
    MFSA.add_arc(MinimizeState([State("e"), State("c"), State("d")]), 1, MinimizeState([State("e"), State("c"), State("d")]), w=Boolean(True))
    MFSA.add_arc(MinimizeState([State("f")]), 2, MinimizeState([State("f")]), w=Boolean(True))
    MFSA.add_arc(MinimizeState([State("f")]), 1, MinimizeState([State("f")]), w=Boolean(True))
    MFSA.add_arc(MinimizeState([State("b"), State("a")]), 1, MinimizeState([State("b"), State("a")]), w=Boolean(True))
    MFSA.add_arc(MinimizeState([State("b"), State("a")]), 2, MinimizeState([State("e"), State("c"), State("d")]), w=Boolean(True))
    # add final states
    MFSA.add_F(MinimizeState([State("e"), State("c"), State("d")]), w=Boolean(True))

    #Temporary assertion
    assert len(mfsa.Q) == len(MFSA.Q)

def test_weighted_equivalence():
    pass