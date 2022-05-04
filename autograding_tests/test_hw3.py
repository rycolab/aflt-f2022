from rayuela.base.misc import components_to_list, is_topologically_sorted_list
from rayuela.fsa.fsa import FSA
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



def test_kosajaru_example():

    components = [frozenset({State(3)}),
                frozenset({State(5)}),
                frozenset({State(7)}),
                frozenset({State(2)}),
                frozenset({State(8)})]
    sccs = SCC(fsa)

    gt = components_to_list(components)
    computed = components_to_list(list(sccs.scc()))
    
    # All elements are present
    assert all([elem in gt for elem in computed]) and all([elem in computed for elem in gt])
    # Computed components are topologically sorted
    assert is_topologically_sorted_list(computed, fsa)

    
    
    
def test_kosajaru():
    with open(f"{hw_path}/sccs.pkl", 'rb') as f:
        sccs = pickle.load(f)
    for fsa, scc in zip(fsas, sccs):
        
        # Only tested for acyclic fsas. Will be updated in future versions.
        if not fsa.acyclic:
            continue
        sccs_fsa = SCC(fsa)

        gt = components_to_list(scc)
        computed = components_to_list(list(sccs_fsa.scc()))
        

        # All elements are present
        assert all([elem in gt for elem in computed]) and all([elem in computed for elem in gt])

        # Computed components are topologically sorted
        assert is_topologically_sorted_list(computed, fsa)

        


def test_decomposed_lehman_example():
   
    assert np.allclose(float(Pathsum(fsa).pathsum(strategy=Strategy.DECOMPOSED_LEHMANN)),float(Real(0.0756)), atol=1e-3)

def test_decomposed_lehman():
    with open(f"{hw_path}/pathsums.pkl", 'rb') as f:
        pathsums = pickle.load(f)
    for fsa, pathsum in zip(fsas, pathsums):
        assert np.allclose(float(Pathsum(fsa).pathsum(strategy=Strategy.DECOMPOSED_LEHMANN)),float(pathsum), atol=1e-3)