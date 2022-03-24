from rayuela.fsa.fsa import FSA
import pickle
from rayuela.base.semiring import Tropical, Real
from rayuela.fsa.state import State
from rayuela.base.symbol import Sym, ε



# TODO: 
# - Examples
# - Edge cases
# - Extend random machines to other semirings

pickles_path = "autograding_tests/pickles"
hw_path = pickles_path + "/hw1"

with open(f"{pickles_path}/fsas.pkl", 'rb') as f:
    fsas = pickle.load(f)



##########################
##### Testing deterministic algorithm
##########################

def test_deterministic():
    with open(f"{hw_path}/deterministic_results.pkl", 'rb') as f:
        deterministic_results = pickle.load(f)
    for fsa, result in zip(fsas, deterministic_results):
        assert fsa.deterministic == result


def test_non_deterministic_example_1():
    """
    Test case from Allauzen and Mohri (2003) Figure 1
    https://cs.nyu.edu/~mohri/pub/twins.pdf
    """
    F = FSA(R=Tropical)
    F.set_I(State(0), F.R(1.0))

    F.add_arc(State(0), Sym('a'), State(1), F.R(1.0))
    F.add_arc(State(0), Sym('a'), State(2), F.R(2.0))

    F.add_arc(State(1), Sym('b'), State(1), F.R(3.0))
    F.add_arc(State(1), Sym('c'), State(3), F.R(5.0))

    F.add_arc(State(2), Sym('b'), State(2), F.R(3.0))
    F.add_arc(State(2), Sym('d'), State(3), F.R(6.0))

    F.add_F(State(3), F.R.one)

    assert F.deterministic == False

def test_deterministic_example_1():
    
    Sigma = set([ε, Sym("a"), Sym("b")])

    fsa = FSA(R=Tropical)

    fsa.add_arc(State(0), 1, State(1), w=Tropical(1.0))
    fsa.add_arc(State(1), 1, State(1), w=Tropical(3.0))
    fsa.add_arc(State(1), 2, State(3), w=Tropical(5.0))


    fsa.set_I(State(0), w=Tropical.one)
    fsa.add_F(State(3), w=Tropical.one)

    assert fsa.deterministic == True

def test_non_deterministic_example_2():
    # From link.springer.com/content/pdf/10.1007/978-3-642-01492-5_6.pdf Example 11a

    Sigma = {0: "eps", 1: "a", 2: "b", 3: "c", 4: "d"}

    fsa = FSA(R=Real)

    fsa.add_arc(State(0), Sigma[1], State(1), w=Real(1))
    fsa.add_arc(State(0), Sigma[1], State(2), w=Real(2))

    fsa.add_arc(State(1), Sigma[2], State(1), w=Real(3))
    fsa.add_arc(State(1), Sigma[3], State(3), w=Real(5))

    fsa.add_arc(State(2), Sigma[2], State(2), w=Real(3))
    fsa.add_arc(State(2), Sigma[4], State(3), w=Real(6))

    # add initial and final states
    fsa.set_I(State(0), w= fsa.R.one)
    fsa.add_F(State(3), w=Real(0))

    assert fsa.deterministic == False

def test_deterministic_example_2():
    # From link.springer.com/content/pdf/10.1007/978-3-642-01492-5_6.pdf Example 11b
    # Determinized version of example 11a

    Sigma = {0: "eps", 1: "a", 2: "b", 3: "c", 4: "d"}

    states = [
        State(0, label=(0, 0)),
        State(1, label=((1, 0), (2, 1))),
        State(2, label=(3, 0)),
    ]

    fsa = FSA(R=Real)

    fsa.add_arc(states[0], Sigma[1], states[1], w=Real(1))

    fsa.add_arc(states[1], Sigma[2], states[1], w=Real(3))
    fsa.add_arc(states[1], Sigma[3], states[2], w=Real(5))
    fsa.add_arc(states[1], Sigma[4], states[2], w=Real(7))

    # add initial & final states
    fsa.set_I(states[0], w=fsa.R.one)
    fsa.add_F(states[2], w=fsa.R.zero)

    assert fsa.deterministic == True

def test_non_deterministic_example_3():
    # From link.springer.com/content/pdf/10.1007/978-3-642-01492-5_6.pdf Example 11c
    # Non-determinizable weighted automaton over the tropical semiring, states 1 and 2 are non-twin siblings

    Sigma = {0: "eps", 1: "a", 2: "b", 3: "c", 4: "d"}

    fsa = FSA(R=Real)

    fsa.add_arc(State(0), Sigma[1], State(1), w=Real(1))
    fsa.add_arc(State(0), Sigma[1], State(2), w=Real(2))

    fsa.add_arc(State(1), Sigma[2], State(1), w=Real(3))
    fsa.add_arc(State(1), Sigma[3], State(3), w=Real(5))

    fsa.add_arc(State(2), Sigma[2], State(2), w=Real(3))
    fsa.add_arc(State(2), Sigma[4], State(3), w=Real(6))

    # add initial and final states
    fsa.set_I(State(0), w= fsa.R.one)
    fsa.add_F(State(3), w=Real(0))

    assert fsa.deterministic == False


##########################
##### Testing pushed algorithm
##########################

def test_pushed():
    with open(f"{hw_path}/pushed_fsas.pkl", 'rb') as f:
        pushed_fsas = pickle.load(f)
    with open(f"{hw_path}/pushed_results.pkl", 'rb') as f:
        pushed_results = pickle.load(f)

    for gt_fsa, result in zip(pushed_fsas, pushed_results):
        assert gt_fsa.pushed == result


def test_not_pushed_example_1():
    # Figure 1: https://www.isca-speech.org/archive/pdfs/eurospeech_2001/mohri01_eurospeech.pdf
    Sigma = {0: "eps", 1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f"}

    fsa = FSA(R=Tropical)

    fsa.set_I(State(0), w=Tropical.one)

    # arcs from state 0
    fsa.add_arc(State(0), 1, State(1), w=Tropical(0.0))
    fsa.add_arc(State(0), 2, State(1), w=Tropical(1.0))
    fsa.add_arc(State(0), 3, State(1), w=Tropical(4.0))
    fsa.add_arc(State(0), 4, State(2), w=Tropical(0.0))
    fsa.add_arc(State(0), 5, State(2), w=Tropical(1.0))

    # arcs from state 1
    fsa.add_arc(State(1), 5, State(3), w=Tropical(0.0))
    fsa.add_arc(State(1), 6, State(3), w=Tropical(1.0))

    # arcs from state 2
    fsa.add_arc(State(2), 5, State(3), w=Tropical(10.0))
    fsa.add_arc(State(2), 6, State(3), w=Tropical(11.0))

    # add final
    fsa.add_F(State(3), w=Tropical(0.0))

    assert fsa.pushed == False

def test_pushed_example_1():
    # Figure 2: https://www.isca-speech.org/archive/pdfs/eurospeech_2001/mohri01_eurospeech.pdf
    
    Sigma = {0: "eps", 1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f"}

    fsa = FSA(R=Tropical)

    fsa.set_I(State(0), w=Tropical.one)

    # arcs from state 0
    fsa.add_arc(State(0), 1, State(1), w=Tropical(0.0))
    fsa.add_arc(State(0), 2, State(1), w=Tropical(1.0))
    fsa.add_arc(State(0), 3, State(1), w=Tropical(4.0))
    fsa.add_arc(State(0), 4, State(2), w=Tropical(10.0))
    fsa.add_arc(State(0), 5, State(2), w=Tropical(11.0))

    # arcs from state 1
    fsa.add_arc(State(1), 5, State(3), w=Tropical(0.0))
    fsa.add_arc(State(1), 6, State(3), w=Tropical(1.0))

    # arcs from state 2
    fsa.add_arc(State(2), 5, State(3), w=Tropical(0.0))
    fsa.add_arc(State(2), 6, State(3), w=Tropical(1.0))

    # add final
    fsa.add_F(State(3), w=Tropical(0.0))

    assert fsa.pushed == True   

def test_not_pushed_example_2():
    # Example 12a: https://link.springer.com/content/pdf/10.1007/978-3-642-01492-5_6.pdf
    Sigma = {0: "eps", 1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f"}

    fsa = FSA(R=Real)

    fsa.add_arc(State(0), Sigma[1], State(1), w=Real(0))
    fsa.add_arc(State(0), Sigma[2], State(1), w=Real(1))
    fsa.add_arc(State(0), Sigma[3], State(1), w=Real(5))
    fsa.add_arc(State(0), Sigma[4], State(2), w=Real(0))
    fsa.add_arc(State(0), Sigma[5], State(2), w=Real(1))

    fsa.add_arc(State(1), Sigma[5], State(3), w=Real(0))
    fsa.add_arc(State(1), Sigma[6], State(3), w=Real(1))

    fsa.add_arc(State(2), Sigma[5], State(3), w=Real(4))
    fsa.add_arc(State(2), Sigma[6], State(3), w=Real(5))

    # add initial & final states
    fsa.set_I(State(0), w=fsa.R.one)
    fsa.add_F(State(3), w=fsa.R.one)

    assert fsa.pushed == False

def test_pushed_example_2():
    # Example 12c: https://link.springer.com/content/pdf/10.1007/978-3-642-01492-5_6.pdf
    
    Sigma = {0: "eps", 1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f"}

    fsa = FSA(R=Real)

    fsa.add_arc(State(0), Sigma[1], State(1), w=Real(0/15))
    fsa.add_arc(State(0), Sigma[2], State(1), w=Real(1/15))
    fsa.add_arc(State(0), Sigma[3], State(1), w=Real(5/15))
    fsa.add_arc(State(0), Sigma[4], State(2), w=Real(0/15))
    fsa.add_arc(State(0), Sigma[5], State(2), w=Real(9/15))

    fsa.add_arc(State(1), Sigma[5], State(3), w=Real(0))
    fsa.add_arc(State(1), Sigma[6], State(3), w=Real(1))

    fsa.add_arc(State(2), Sigma[5], State(3), w=Real(4/9))
    fsa.add_arc(State(2), Sigma[6], State(3), w=Real(5/9))

    # add initial & final states
    fsa.set_I(State(0), w=Real(15))
    fsa.add_F(State(3), w=Real(1))

    assert fsa.pushed == True   


##########################
##### Testing reverse algorithm
##########################

def test_reverse_string():
    # TODO: show that for any string x∈Σ∗ accepted by the original automaton, ←−xis accepted by its reversal
    pass

def test_reverse():
    
    with open(f"{hw_path}/reversed_fsas_ascii.pkl", 'rb') as f:
        reversed_asciis = pickle.load(f)
    
    for fsa, rfsa in zip(fsas, reversed_asciis):
        assert fsa.reverse().__str__() == rfsa

##########################
##### Testing accessible & coaccessible algorithms
##########################

def test_accessible():
    
    with open(f"{hw_path}/accessible_states.pkl", 'rb') as f:
        accessible_states_fsas = pickle.load(f)
    
    for fsa, accessible_states in zip(fsas, accessible_states_fsas):
        assert fsa.accessible() == accessible_states

def test_coaccessible():
    
    with open(f"{hw_path}/coaccessible_states.pkl", 'rb') as f:
        coaccessible_states_fsas = pickle.load(f)
    
    for fsa, coaccessible_states in zip(fsas, coaccessible_states_fsas):
        assert fsa.coaccessible() == coaccessible_states

##########################
##### Testing trim algorithm
##########################

def test_trim():
    # TODO
    pass


##########################
##### Testing union algorithm
##########################

def test_union():
    with open(f"{hw_path}/union_fsas.pkl", 'rb') as f:
        union_fsas = pickle.load(f)
    
    middle = int(len(fsas)/2)
    for left_fsa, right_fsa, union_fsa in zip(fsas[:middle], fsas[middle:], union_fsas):
        assert left_fsa.union(right_fsa).__str__() == union_fsa.__str__()

##########################
##### Testing concatenate algorithm
##########################

def test_concatenate():
    with open(f"{hw_path}/concat_fsas.pkl", 'rb') as f:
        concat_fsas = pickle.load(f)
    
    middle = int(len(fsas)/2)
    for left_fsa, right_fsa, concat_fsa in zip(fsas[:middle], fsas[middle:], concat_fsas):
        assert left_fsa.concatenate(right_fsa).__str__() == concat_fsa.__str__()

##########################
##### Testing Kleene closure algorithm
##########################


def test_closure():
    with open(f"{hw_path}/kleene_fsas.pkl", 'rb') as f:
        kleene_fsas = pickle.load(f)
    
    for fsa, kleene in zip(fsas, kleene_fsas):
        assert fsa.kleene_closure().__str__() == kleene.__str__()
