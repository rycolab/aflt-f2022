from rayuela.fsa.fsa import FSA
from rayuela.base.semiring import Tropical, Real
from rayuela.fsa.state import PairState, State
from rayuela.base.symbol import Sym, ε
from rayuela.fsa.scc import SCC
from rayuela.fsa.pathsum import Pathsum, Strategy
import pickle

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

    assert components == list(sccs.scc())
    
    
def test_kosajaru():
    with open(f"{hw_path}/sccs.pkl", 'rb') as f:
        sccs = pickle.load(f)
    for fsa, scc in zip(fsas, sccs):
        sccs_fsa = SCC(fsa)
        assert list(sccs_fsa.scc()) == list(scc.scc())


def test_decomposed_lehman_example():

    assert Real(0.0756) == Pathsum(fsa).pathsum(strategy=Strategy.DECOMPOSED_LEHMANN)

def test_decomposed_lehman():
    with open(f"{hw_path}/pathsums.pkl", 'rb') as f:
        pathsums = pickle.load(f)
    for fsa, pathsum in zip(fsas, pathsums):
        assert Pathsum(fsa).pathsum(strategy=Strategy.DECOMPOSED_LEHMANN) == pathsum