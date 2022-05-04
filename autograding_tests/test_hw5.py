from rayuela.fsa.fsa import FSA
from rayuela.base.semiring import Boolean, Tropical, Real
from rayuela.fsa.state import MinimizeState, PairState, State, PowerState
from rayuela.base.symbol import Sym, ε
from rayuela.fsa.scc import SCC
from rayuela.fsa.pathsum import Pathsum, Strategy
import pickle
from rayuela.base.misc import compare_fsas, compare_charts, same_number_of_arcs
import numpy as np

pickles_path = "autograding_tests/pickles"
hw_path = pickles_path + "/hw5"

with open(f"{hw_path}/fsas.pkl", 'rb') as f:
    fsas = pickle.load(f)

def test_bellman_ford():
    with open(f"{hw_path}/bellmanford_fwd.pkl", 'rb') as f:
        αs = pickle.load(f)

    for fsa, α in zip(fsas, αs):

        computed_alpha = Pathsum(fsa).forward(Strategy.BELLMANFORD)

        assert compare_charts(α, computed_alpha)

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
    
    assert len(mfsa.Q) == len(MFSA.Q) 
    assert same_number_of_arcs(mfsa, MFSA)

def test_weighted_equivalence():
    # pass a bunch of previous tests using the equivalet method instead of comparing the pathsums
    
    with open(f"{pickles_path}/fsas.pkl", 'rb') as f:
        fsas = pickle.load(f)
    # HW1

    hw_path = pickles_path + "/hw1"
    # Reversed fsas
    with open(f"{hw_path}/reversed_fsas.pkl", 'rb') as f:
        reversed_fsas = pickle.load(f)
    
    for fsa, rfsa in zip(fsas, reversed_fsas):
        assert rfsa.equivalent(fsa.reverse())

    # Union
    with open(f"{hw_path}/union_fsas.pkl", 'rb') as f:
        union_fsas = pickle.load(f)
    
    middle = int(len(fsas)/2)
    for left_fsa, right_fsa, union_fsa in zip(fsas[:middle], fsas[middle:], union_fsas):
        assert union_fsa.equivalent(left_fsa.union(right_fsa))

    # Concat
    with open(f"{hw_path}/concat_fsas.pkl", 'rb') as f:
        concat_fsas = pickle.load(f)
    
    middle = int(len(fsas)/2)
    for left_fsa, right_fsa, concat_fsa in zip(fsas[:middle], fsas[middle:], concat_fsas):
        assert concat_fsa.equivalent(left_fsa.concatenate(right_fsa))

    # Kleene closure
    with open(f"{hw_path}/kleene_fsas.pkl", 'rb') as f:
        kleene_fsas = pickle.load(f)
    
    for fsa, kleene in zip(fsas, kleene_fsas):
        assert kleene.equivalent(fsa.kleene_closure())

        

def test_equivalence_example():
    TRIMMED = FSA(Real)

    TRIMMED.add_arc(State(0), Sym('b'), State(1), w=Real(0.1))


    TRIMMED.add_arc(State(1), Sym('b'), State(1), w=Real(0.2))
    TRIMMED.add_arc(State(1), Sym('a'), State(2), w=Real(0.3))
    TRIMMED.add_arc(State(1), Sym('a'), State(3), w=Real(0.4))


    TRIMMED.add_arc(State(2), Sym('b'), State(3), w=Real(0.5))

    TRIMMED.set_I(State(0), w=Real(1.0))
    TRIMMED.add_F(State(3), w=Real(0.6))


    NOT_TRIMMED_FSA = FSA(Real)

    NOT_TRIMMED_FSA.add_arc(State(0), Sym('b'), State(1), w=Real(0.1))


    NOT_TRIMMED_FSA.add_arc(State(1), Sym('b'), State(1), w=Real(0.2))
    NOT_TRIMMED_FSA.add_arc(State(1), Sym('a'), State(2), w=Real(0.3))
    NOT_TRIMMED_FSA.add_arc(State(1), Sym('a'), State(3), w=Real(0.4))
    NOT_TRIMMED_FSA.add_arc(State(1), Sym('a'), State(5), w=Real(0.4))


    NOT_TRIMMED_FSA.add_arc(State(2), Sym('b'), State(3), w=Real(0.5))

    NOT_TRIMMED_FSA.add_arc(State(4), Sym('b'), State(3), w=Real(0.5))

    NOT_TRIMMED_FSA.set_I(State(0), w=Real(1.0))
    NOT_TRIMMED_FSA.add_F(State(3), w=Real(0.6))

    assert TRIMMED.equivalent(NOT_TRIMMED_FSA)