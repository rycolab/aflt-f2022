from rayuela.fsa.fsa import FSA
from rayuela.base.semiring import Tropical, Real
from rayuela.fsa.state import PairState, State, PowerState
from rayuela.base.symbol import Sym, ε
from rayuela.fsa.scc import SCC
from rayuela.fsa.pathsum import Pathsum, Strategy
import pickle
from rayuela.base.misc import compare_fsas

pickles_path = "autograding_tests/pickles"
hw_path = pickles_path + "/hw4"


def test_determinization_example():
    """
    Test case from Allauzen and Mohri (2003) Figure 1
    https://cs.nyu.edu/~mohri/pub/twins.pdf
    """

    fsa = FSA(R=Tropical)
		
    fsa.add_arc(State(0), 1, State(1), w=Tropical(1.0))
    fsa.add_arc(State(0), 1, State(2), w=Tropical(2.0))
    
    fsa.add_arc(State(1), 2, State(1), w=Tropical(3.0))
    fsa.add_arc(State(1), 3, State(3), w=Tropical(5.0))

    fsa.add_arc(State(2), 2, State(2), w=Tropical(3.0))
    fsa.add_arc(State(2), 4, State(3), w=Tropical(6.0))
    
    fsa.set_I(State(0), w=Tropical.one)
    fsa.add_F(State(3), w=Tropical.one)

    dfsa = fsa.determinize()

    DFSA = FSA(R=Tropical)

    DFSA.add_arc(PowerState({State(1): Tropical(0.0), State(2): Tropical(1.0)}), 2, PowerState({State(1): Tropical(0.0), State(2): Tropical(1.0)}), w=Tropical(3.0))
    DFSA.add_arc(PowerState({State(1): Tropical(0.0), State(2): Tropical(1.0)}), 3, PowerState({State(3): Tropical(0.0)}), w=Tropical(5.0))
    DFSA.add_arc(PowerState({State(1): Tropical(0.0), State(2): Tropical(1.0)}), 4, PowerState({State(3): Tropical(0.0)}), w=Tropical(7.0))
    DFSA.add_arc(PowerState({State(0): Tropical(0.0)}), 1, PowerState({State(1): Tropical(0.0), State(2): Tropical(1.0)}), w=Tropical(1.0))


    DFSA.set_I(PowerState({State(0): Tropical(0.0)}), w=Tropical.one)
    DFSA.add_F(PowerState({State(3): Tropical(0.0)}), w=Tropical.one)

    assert compare_fsas(DFSA, dfsa)
    assert dfsa.deterministic

def test_determinization():
    with open(f"{hw_path}/determinized_fsas.pkl", 'rb') as f:
        dfsas = pickle.load(f)
    with open(f"{hw_path}/determinizable_fsas.pkl", 'rb') as f:
        fsas = pickle.load(f)

    for fsa, dfsa in zip(fsas, dfsas):
        determinized = fsa.determinize()
        assert compare_fsas(dfsa, determinized)
        assert determinized.deterministic
        

