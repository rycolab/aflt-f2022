from rayuela.base.misc import compare_fsas, is_topologically_sorted_scc
from rayuela.fsa.fsa import FSA
from rayuela.fsa.fst import FST
from rayuela.base.semiring import Tropical, Real
from rayuela.fsa.state import PairState, State
from rayuela.base.symbol import Sym, ε
from rayuela.fsa.scc import SCC
from rayuela.fsa.pathsum import Pathsum, Strategy
import pickle
import numpy as np

pickles_path = "autograding_tests/pickles"
hw_path = pickles_path + "/hw3"

with open(f"{pickles_path}/fsas.pkl", 'rb') as f:
    fsas = pickle.load(f)

fsa = FSA(R=Real)

fsa.add_arc(State(2), Sym('a'), State(8), Real(0.1))

fsa.add_arc(State(3), Sym('c'), State(5), Real(0.4))
fsa.add_arc(State(3), Sym('a'), State(7), Real(0.7))

fsa.add_arc(State(5), Sym('a'), State(2), Real(0.3))
fsa.add_arc(State(5), Sym('a'), State(7), Real(0.8))

fsa.set_I(State(3), Real(0.3))
fsa.set_F(State(2), Real(0.4))
fsa.set_F(State(7), Real(0.2))



def test_kosajaru_example_1():

    components = [frozenset({State(3)}),
                frozenset({State(5)}),
                frozenset({State(7)}),
                frozenset({State(2)}),
                frozenset({State(8)})]
    sccs = SCC(fsa)

    gt = components
    computed = list(sccs.scc())

    # All elements are present
    assert all([elem in gt for elem in computed]) and all([elem in computed for elem in gt])
    # Computed components are topologically sorted
    assert is_topologically_sorted_scc(computed, fsa)

def test_kosajaru_example_2():
    F = FSA(R=Real)
    F.set_I(State(0), F.R(1 / 2))

    F.add_arc(State(0), Sym('a'), State(1), F.R(1 / 2.0))
    F.add_arc(State(0), Sym('a'), State(2), F.R(1 / 5.0))

    F.add_arc(State(1), Sym('b'), State(1), F.R(1 / 8.0))
    F.add_arc(State(1), Sym('c'), State(3), F.R(1 / 10.0))

    F.add_arc(State(2), Sym('d'), State(3), F.R(1 / 5.0))

    F.add_arc(State(3), Sym('b'), State(2), F.R(1 / 10.0))

    F.add_F(State(3), F.R(1 / 4))

    components = [frozenset({State(0)}), frozenset({State(1)}), frozenset({State(2), State(3)})]

    gt = components
    computed = list(SCC(F).scc())
    
    # All elements are present
    assert all([elem in gt for elem in computed]) and all([elem in computed for elem in gt])
    # Computed components are topologically sorted. As fsa is not acyclic, there is no topological order.
    # assert is_topologically_sorted_scc(computed, F)

def test_kosajaru_example_3():
    F = FSA(R=Real)
    F.set_I(State(0), F.R(1 / 2))

    F.add_arc(State(0), Sym('a'), State(1), F.R(1 / 2.0))
    F.add_arc(State(0), Sym('a'), State(2), F.R(1 / 5.0))

    F.add_arc(State(1), Sym('c'), State(3), F.R(1 / 10.0))
    F.add_arc(State(1), Sym('c'), State(4), F.R(1 / 10.0))

    F.add_arc(State(2), Sym('d'), State(3), F.R(1 / 5.0))
    F.add_arc(State(2), Sym('c'), State(5), F.R(1 / 10.0))

    F.add_arc(State(3), Sym('b'), State(2), F.R(1 / 10.0))

    F.add_arc(State(4), Sym('c'), State(1), F.R(1 / 10.0))

    F.add_arc(State(5), Sym('c'), State(3), F.R(1 / 10.0))

    F.add_F(State(3), F.R(1 / 4))

    components = [frozenset({State(0)}), frozenset({State(1), State(4)}), frozenset({State(2), State(3), State(5)})]

    gt = components
    computed = list(SCC(F).scc())
    
    # All elements are present
    assert all([elem in gt for elem in computed]) and all([elem in computed for elem in gt])
    # Computed components are topologically sorted. As fsa is not acyclic, there is no topological order.
    # assert is_topologically_sorted_scc(computed, F)
    
    
def test_kosajaru():
    with open(f"{hw_path}/sccs.pkl", 'rb') as f:
        sccs = pickle.load(f)
    for fsa, scc in zip(fsas, sccs):
        
        # Topological order only exists for acyclic fsas. 
        if not fsa.acyclic:
            continue
        sccs_fsa = SCC(fsa)

        gt = scc
        computed = list(sccs_fsa.scc())
        

        # All elements are present
        assert all([elem in gt for elem in computed]) and all([elem in computed for elem in gt])

        # Computed components are topologically sorted. Only check if there are more than 1 SCC (there's no orden in a list of only one element)
        if len(computed) > 1:
            assert is_topologically_sorted_scc(computed, fsa)

        


def test_decomposed_lehman_example():
   
    assert np.allclose(float(Pathsum(fsa).pathsum(strategy=Strategy.DECOMPOSED_LEHMANN)),float(Real(0.0756)), atol=1e-3)

def test_decomposed_lehman():
    with open(f"{hw_path}/pathsums.pkl", 'rb') as f:
        pathsums = pickle.load(f)
    for fsa, pathsum in zip(fsas, pathsums):
        assert np.allclose(float(Pathsum(fsa).pathsum(strategy=Strategy.DECOMPOSED_LEHMANN)),float(pathsum), atol=1e-3)

def test_top_composition_example():
    # Initilize directly with the semiring we want
    fst1 = FST(Real)

    # We add *two* symbols per arc and the weight directly in the semiring itself
    fst1.add_arc(State(0), Sym('d'), Sym('data'), State(1), Real(0.5))
    fst1.add_arc(State(0), Sym('d'), Sym('dew'), State(5), Real(0.5))

    fst1.add_arc(State(1), Sym('ey'), Sym('y'), State(2), Real(0.5))
    fst1.add_arc(State(1), Sym('ae'), Sym('æ'), State(2), Real(0.5))

    fst1.add_arc(State(2), Sym('t'), Sym('τ'), State(3), Real(0.7))
    fst1.add_arc(State(2), Sym('DX'), Sym('D'), State(3), Real(0.3))

    fst1.add_arc(State(3), Sym('AX'), Sym('χ'), State(4), Real(1.0))

    fst1.add_arc(State(5), Sym('uw'), Sym('ch'), State(6), Real(1.0))

    fst1.set_I(State(0))
    fst1.set_F(State(4))
    fst1.set_F(State(6))

    # Initilize directly with the semiring we want
    fst2 = FST(Real)

    # We add *two* symbols per arc and the weight directly in the semiring itself
    fst2.add_arc(State(0), Sym('data'), Sym('DATOS'), State(1), Real(0.5))
    fst2.add_arc(State(0), Sym('dew'), Sym('D'), State(5), Real(0.5))

    fst2.add_arc(State(1), Sym('y'), Sym('EY'), State(2), Real(0.5))
    fst2.add_arc(State(1), Sym('æ'), Sym('AE'), State(2), Real(0.5))

    fst2.add_arc(State(2), Sym('τ'), Sym('T'), State(3), Real(0.7))
    fst2.add_arc(State(2), Sym('D'), Sym('DX'), State(6), Real(0.3))

    fst2.add_arc(State(3), Sym('χ'), Sym('AX'), State(4), Real(1.0))

    fst2.add_arc(State(5), Sym('ch'), Sym('UW'), State(6), Real(1.0))

    fst2.set_I(State(0))
    fst2.set_F(State(4))
    fst2.set_F(State(6))

    # Initilize directly with the semiring we want
    TOP = FST(Real)

    # We add *two* symbols per arc and the weight directly in the semiring itself
    TOP.add_arc(PairState(State(0),State(0)), Sym('d'), Sym('DATOS'), PairState(State(1),State(1)), Real(0.25))
    TOP.add_arc(PairState(State(0),State(0)), Sym('d'), Sym('D'), PairState(State(5),State(5)), Real(0.25))


    TOP.add_arc(PairState(State(5),State(5)), Sym('uw'), Sym('UW'), PairState(State(6),State(6)), Real(1.0))
    TOP.add_arc(PairState(State(1),State(1)), Sym('ey'), Sym('EY'), PairState(State(2),State(2)), Real(0.25))
    TOP.add_arc(PairState(State(1),State(1)), Sym('ae'), Sym('AE'), PairState(State(2),State(2)), Real(0.25))
    TOP.add_arc(PairState(State(3),State(3)), Sym('AX'), Sym('AX'), PairState(State(4),State(4)), Real(1.0))
    TOP.add_arc(PairState(State(2),State(2)), Sym('t'), Sym('T'), PairState(State(3),State(3)), Real(0.49))
    # TOP.add_arc(PairState(State(2),State(2)), Sym('DX'), Sym('DX'), PairState(State(3),State(6)), Real(0.09))

    TOP.set_I(PairState(State(0),State(0)))
    TOP.set_F(PairState(State(4),State(4)))
    TOP.set_F(PairState(State(6),State(6)))

    top = fst1.top_compose(fst2).trim()
    
    # TODO: Not sure if this is the best assertion. Specially interested in checking the labels
    # assert top.trim().__str__() == TOP.trim().__str__()
    # for q1, q2 in zip(top.Q, TOP.Q):
    #     assert list(top.arcs(q1)) == list(TOP.arcs(q2))
    assert compare_fsas(TOP, top)

def test_composition():

    with open(f"{hw_path}/top_composition.pkl", 'rb') as f:
        top_composition = pickle.load(f)
    with open(f"{hw_path}/bottom_composition.pkl", 'rb') as f:
        bottom_composition = pickle.load(f)

    try:
        top_compose_works = all([compare_fsas(top, left.top_compose(right)) for top, left, right in top_composition])
    except:
        top_compose_works = False
    try:
        bottom_compose_works = all([compare_fsas(top, left.bottom_compose(right)) for top, left, right in bottom_composition])
    except: 
        bottom_compose_works = False

    assert top_compose_works or bottom_compose_works
