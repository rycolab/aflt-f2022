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

def test_minimization_example_1():
    fsa = FSA(R=Boolean)
    fsa.set_I(State("a"), w=Boolean(True))

    # arcs from state a
    fsa.add_arc(State("a"), 1, State("b"), w=Boolean(True))
    fsa.add_arc(State("a"), 2, State("c"), w=Boolean(True))

    # arcs from state b
    fsa.add_arc(State("b"), 2, State("d"), w=Boolean(True))
    fsa.add_arc(State("b"), 1, State("a"), w=Boolean(True))

    # arcs from state c
    fsa.add_arc(State("c"), 1, State("e"), w=Boolean(True))

    # arcs from state d
    fsa.add_arc(State("d"), 1, State("e"), w=Boolean(True))

    # arcs from state e
    fsa.add_arc(State("e"), 1, State("e"), w=Boolean(True))

    # add final states
    fsa.add_F(State("c"), w=Boolean(True))
    fsa.add_F(State("d"), w=Boolean(True))
    fsa.add_F(State("e"), w=Boolean(True))

    mfsa = fsa.minimize()

    MFSA = FSA(R=Boolean)
    MFSA.set_I(MinimizeState([State("b"), State("a")]), w=Boolean(True))
    MFSA.add_arc(MinimizeState([State("e"), State("c"), State("d")]), 1, MinimizeState([State("e"), State("c"), State("d")]), w=Boolean(True))
    MFSA.add_arc(MinimizeState([State("b"), State("a")]), 2, MinimizeState([State("e"), State("c"), State("d")]), w=Boolean(True))
    MFSA.add_arc(MinimizeState([State("b"), State("a")]), 1, MinimizeState([State("b"), State("a")]), w=Boolean(True))
    # add final states
    MFSA.add_F(MinimizeState([State("e"), State("c"), State("d")]), w=Boolean(True))

    
    assert len(mfsa.Q) == len(MFSA.Q) 
    assert same_number_of_arcs(mfsa, MFSA)

def test_minimization_example_2():
    
    """
    Test case from Revuz (1991)
    """

    fsa = FSA(Boolean)
    fsa.set_I(State(1), Boolean(True))

    fsa.add_arc(State(1), "a", State(2), Boolean(True))
    fsa.add_arc(State(1), "b", State(3), Boolean(True))
    fsa.add_arc(State(1), "c", State(4), Boolean(True))

    fsa.add_arc(State(2), "a", State(5), Boolean(True))
    fsa.add_arc(State(2), "b", State(6), Boolean(True))

    fsa.add_arc(State(3), "a", State(10), Boolean(True))
    fsa.add_arc(State(3), "b", State(7), Boolean(True))

    fsa.add_arc(State(4), "a", State(8), Boolean(True))
    fsa.add_arc(State(4), "b", State(9), Boolean(True))

    fsa.add_arc(State(5), "a", State(15), Boolean(True))
    fsa.add_arc(State(5), "b", State(10), Boolean(True))

    fsa.add_arc(State(6), "a", State(10), Boolean(True))
    fsa.add_arc(State(6), "b", State(11), Boolean(True))

    fsa.add_arc(State(7), "a", State(10), Boolean(True))
    fsa.add_arc(State(7), "b", State(11), Boolean(True))

    fsa.add_arc(State(8), "a", State(12), Boolean(True))

    fsa.add_arc(State(9), "a", State(12), Boolean(True))
    fsa.add_arc(State(9), "b", State(15), Boolean(True))

    fsa.add_arc(State(10), "a", State(13), Boolean(True))
    fsa.add_arc(State(10), "b", State(15), Boolean(True))

    fsa.add_arc(State(11), "a", State(13), Boolean(True))

    fsa.add_arc(State(12), "a", State(14), Boolean(True))
    fsa.add_arc(State(12), "c", State(15), Boolean(True))

    fsa.add_arc(State(13), "b", State(15), Boolean(True))

    fsa.add_arc(State(14), "d", State(15), Boolean(True))

    fsa.add_F(State(15), Boolean(True))

    mfsa = FSA(Boolean)
    mfsa.add_arc(MinimizeState([State(2)]), 'a', MinimizeState([State(5)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(2)]), 'b', MinimizeState([State(6), State(7)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(11)]), 'a', MinimizeState([State(13)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(14)]), 'd', MinimizeState([State(15)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(9)]), 'a', MinimizeState([State(12)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(9)]), 'b', MinimizeState([State(15)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(6), State(7)]), 'a', MinimizeState([State(10)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(6), State(7)]), 'b', MinimizeState([State(11)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(8)]), 'a', MinimizeState([State(12)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(3)]), 'a', MinimizeState([State(10)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(3)]), 'b', MinimizeState([State(6), State(7)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(10)]), 'a', MinimizeState([State(13)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(10)]), 'b', MinimizeState([State(15)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(1)]), 'a', MinimizeState([State(2)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(1)]), 'b', MinimizeState([State(3)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(1)]), 'c', MinimizeState([State(4)]), Boolean(True))
    mfsa.set_I(MinimizeState([State(1)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(13)]), 'b', MinimizeState([State(15)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(5)]), 'a', MinimizeState([State(15)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(5)]), 'b', MinimizeState([State(10)]), Boolean(True))
    mfsa.add_F(MinimizeState([State(15)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(12)]), 'a', MinimizeState([State(14)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(12)]), 'c', MinimizeState([State(15)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(4)]), 'a', MinimizeState([State(8)]), Boolean(True))
    mfsa.add_arc(MinimizeState([State(4)]), 'b', MinimizeState([State(9)]), Boolean(True))

    assert len(mfsa.Q) == len(fsa.minimize().Q) 
    assert same_number_of_arcs(mfsa, fsa.minimize())

def test_minimization_example_3():

    """
    Modified test case from Revuz (1991)
    """

    fsa = FSA(Boolean)
    fsa.set_I(State(1), Boolean(True))

    fsa.add_arc(State(1), "a", State(2), Boolean(True))
    fsa.add_arc(State(1), "b", State(3), Boolean(True))
    fsa.add_arc(State(1), "c", State(4), Boolean(True))

    fsa.add_arc(State(2), "a", State(5), Boolean(True))
    fsa.add_arc(State(2), "b", State(6), Boolean(True))

    fsa.add_arc(State(3), "a", State(10), Boolean(True))
    fsa.add_arc(State(3), "b", State(7), Boolean(True))

    fsa.add_arc(State(4), "a", State(8), Boolean(True))
    fsa.add_arc(State(4), "b", State(9), Boolean(True))

    # fsa.add_arc(State(5), "a", State(15), Boolean(True))
    fsa.add_arc(State(5), "b", State(10), Boolean(True))

    # fsa.add_arc(State(6), "a", State(10), Boolean(True))
    fsa.add_arc(State(6), "b", State(11), Boolean(True))

    fsa.add_arc(State(7), "a", State(10), Boolean(True))
    fsa.add_arc(State(7), "b", State(11), Boolean(True))

    fsa.add_arc(State(8), "a", State(12), Boolean(True))

    fsa.add_arc(State(9), "a", State(12), Boolean(True))

    fsa.add_arc(State(10), "a", State(13), Boolean(True))
    fsa.add_arc(State(10), "b", State(15), Boolean(True))

    fsa.add_arc(State(11), "a", State(13), Boolean(True))
    fsa.add_arc(State(11), "b", State(15), Boolean(True))

    fsa.add_arc(State(12), "a", State(14), Boolean(True))
    fsa.add_arc(State(12), "c", State(15), Boolean(True))

    fsa.add_arc(State(13), "b", State(15), Boolean(True))

    fsa.add_arc(State(14), "d", State(15), Boolean(True))

    fsa.add_F(State(15), Boolean(True))

    MFSA = FSA(Boolean)
    MFSA.add_arc(MinimizeState([State(2)]), 'a', MinimizeState([State(5), State(6)]), Boolean(True))
    MFSA.add_arc(MinimizeState([State(2)]), 'b', MinimizeState([State(5), State(6)]), Boolean(True))
    MFSA.add_arc(MinimizeState([State(14)]), 'd', MinimizeState([State(15)]), Boolean(True))
    MFSA.add_arc(MinimizeState([State(8), State(9)]), 'a', MinimizeState([State(12)]), Boolean(True))
    MFSA.add_F(MinimizeState([State(15)]), Boolean(True))
    MFSA.add_arc(MinimizeState([State(7)]), 'a', MinimizeState([State(10), State(11)]), Boolean(True))
    MFSA.add_arc(MinimizeState([State(7)]), 'b', MinimizeState([State(10), State(11)]), Boolean(True))
    MFSA.add_arc(MinimizeState([State(3)]), 'a', MinimizeState([State(10), State(11)]), Boolean(True))
    MFSA.add_arc(MinimizeState([State(3)]), 'b', MinimizeState([State(7)]), Boolean(True))
    MFSA.add_arc(MinimizeState([State(1)]), 'a', MinimizeState([State(2)]), Boolean(True))
    MFSA.add_arc(MinimizeState([State(1)]), 'b', MinimizeState([State(3)]), Boolean(True))
    MFSA.add_arc(MinimizeState([State(1)]), 'c', MinimizeState([State(4)]), Boolean(True))
    MFSA.set_I(MinimizeState([State(1)]), Boolean(True))
    MFSA.add_arc(MinimizeState([State(5), State(6)]), 'b', MinimizeState([State(10), State(11)]), Boolean(True))
    MFSA.add_arc(MinimizeState([State(13)]), 'b', MinimizeState([State(15)]), Boolean(True))
    MFSA.add_arc(MinimizeState([State(10), State(11)]), 'a', MinimizeState([State(13)]), Boolean(True))
    MFSA.add_arc(MinimizeState([State(10), State(11)]), 'b', MinimizeState([State(15)]), Boolean(True))
    MFSA.add_arc(MinimizeState([State(12)]), 'a', MinimizeState([State(14)]), Boolean(True))
    MFSA.add_arc(MinimizeState([State(12)]), 'c', MinimizeState([State(15)]), Boolean(True))
    MFSA.add_arc(MinimizeState([State(4)]), 'a', MinimizeState([State(8), State(9)]), Boolean(True))
    MFSA.add_arc(MinimizeState([State(4)]), 'b', MinimizeState([State(8), State(9)]), Boolean(True))

    mfsa = fsa.minimize()

    assert len(mfsa.Q) == len(MFSA.Q) 
    assert same_number_of_arcs(mfsa, MFSA)


def test_weighted_equivalence():
    # pass a bunch of previous tests using the equivalet method instead of comparing the pathsums
    
    
    with open(f"{hw_path}/equivalence.pkl", 'rb') as f:
        equivalents = pickle.load(f)
    
    for fsa, rfsa in zip(*equivalents['reverse']):
        assert rfsa.equivalent(fsa.reverse())
    
    for (left_fsa, right_fsa), union_fsa in zip(*equivalents['union']):
        assert union_fsa.equivalent(left_fsa.union(right_fsa))

    for (left_fsa, right_fsa), concat_fsa in zip(*equivalents['concat']):
        assert concat_fsa.equivalent(left_fsa.concatenate(right_fsa))

    for fsa, kleene in zip(*equivalents['kleene']):
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