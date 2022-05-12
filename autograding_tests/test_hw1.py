from rayuela.fsa.fsa import FSA
import pickle
from rayuela.base.semiring import Tropical, Real
from rayuela.fsa.state import PairState, State
from rayuela.base.symbol import Sym, ε
from rayuela.base.misc import compare_fsas


# TODO: 
# - More examples
# - Edge cases
# - Extend random machines to other semirings



pickles_path = "autograding_tests/pickles"
hw_path = pickles_path + "/hw1"

with open(f"{pickles_path}/fsas.pkl", 'rb') as f:
    fsas = pickle.load(f)

FSA1 = FSA(Real)

FSA1.add_arc(State(0), Sym('a'), State(0), w=Real(0.043))
FSA1.add_arc(State(0), Sym('a'), State(1), w=Real(0.147))
FSA1.add_arc(State(0), Sym('b'), State(2), w=Real(0.108))

FSA1.add_arc(State(1), Sym('a'), State(0), w=Real(0.125))
FSA1.add_arc(State(1), Sym('a'), State(2), w=Real(0.026))
FSA1.add_arc(State(1), Sym('b'), State(0), w=Real(0.151))

FSA1.add_arc(State(2), Sym('a'), State(0), w=Real(0.128))
FSA1.add_arc(State(2), Sym('a'), State(2), w=Real(0.088))
FSA1.add_arc(State(2), Sym('b'), State(1), w=Real(0.024))


FSA1.set_I(State(0), w=Real(0.078))
FSA1.add_F(State(2), w=Real(0.156))

FSA2 = FSA(Real)

FSA2.add_arc(State(0), Sym('b'), State(0), w=Real(0.147))
FSA2.add_arc(State(0), Sym('b'), State(1), w=Real(0.136))
FSA2.add_arc(State(0), Sym('b'), State(2), w=Real(0.025))
FSA2.add_arc(State(0), Sym('a'), State(1), w=Real(0.076))
FSA2.add_arc(State(0), Sym('a'), State(2), w=Real(0.159))


FSA2.add_arc(State(1), Sym('b'), State(0), w=Real(0.125))
FSA2.add_arc(State(1), Sym('b'), State(1), w=Real(0.007))
FSA2.add_arc(State(1), Sym('b'), State(2), w=Real(0.074))
FSA2.add_arc(State(1), Sym('a'), State(2), w=Real(0.047))

FSA2.add_arc(State(2), Sym('a'), State(0), w=Real(0.019))
FSA2.add_arc(State(2), Sym('a'), State(2), w=Real(0.084))
FSA2.add_arc(State(2), Sym('b'), State(0), w=Real(0.15))


FSA2.set_I(State(0), w=Real(0.141))
FSA2.add_F(State(2), w=Real(0.062))





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
    T1 = FSA(Real)

    T1.add_arc(State(0), Sym('a'), State(1))

    T1.add_arc(State(1), Sym('b'), State(2))
    T1.add_arc(State(1), Sym('c'), State(3))
    T1.add_arc(State(2), Sym('a'), State(4))
    T1.add_arc(State(3), Sym('d'), State(4))
    T1.add_arc(State(4), Sym('e'), State(4))

    T1.set_I(State(0))
    T1.set_F(State(4))

    reversed_T1 = T1.reverse()

    assert T1.accept("abae") == reversed_T1.accept("eaba")

def test_reverse_example():

    T1 = FSA(Real)

    T1.add_arc(State(0), Sym('a'), State(1), w=Real(0.1))

    T1.add_arc(State(1), Sym('b'), State(2), w=Real(0.3))
    T1.add_arc(State(1), Sym('b'), State(3), w=Real(0.4))
    T1.add_arc(State(1), Sym('a'), State(0), w=Real(0.2))

    T1.add_arc(State(2), Sym('a'), State(3), w=Real(0.5))

    T1.add_arc(State(3), Sym('a'), State(3), w=Real(0.6))

    T1.set_I(State(0), w=Real(1.0))
    T1.add_F(State(3), w=Real(0.7))

    REVERSED = FSA(Real)

    REVERSED.add_arc(State(0), Sym('a'), State(1), w=Real(0.2))

    REVERSED.add_arc(State(1), Sym('a'), State(0), w=Real(0.1))

    REVERSED.add_arc(State(2), Sym('b'), State(1), w=Real(0.3))

    REVERSED.add_arc(State(3), Sym('b'), State(1), w=Real(0.4))
    REVERSED.add_arc(State(3), Sym('a'), State(2), w=Real(0.5))
    REVERSED.add_arc(State(3), Sym('a'), State(3), w=Real(0.6))

    REVERSED.add_F(State(0), w=Real(1.0))
    REVERSED.set_I(State(3), w=Real(0.7))

    assert True == compare_fsas(REVERSED, T1.reverse())

def test_reverse():
    
    with open(f"{hw_path}/reversed_fsas.pkl", 'rb') as f:
        reversed_fsas = pickle.load(f)
    
    for fsa, rfsa in zip(fsas, reversed_fsas):
        assert True == compare_fsas(rfsa, fsa.reverse())

##########################
##### Testing accessible & coaccessible algorithms
##########################

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

def test_accessible_example():

    accessible_states = {State(0),State(1),State(2),State(3),State(5)}

    assert NOT_TRIMMED_FSA.accessible() == accessible_states

def test_coaccessible_example():

    coaccessible_states = {State(0),State(1),State(2),State(3),State(4)}

    assert NOT_TRIMMED_FSA.coaccessible() == coaccessible_states

##########################
##### Testing trim algorithm
##########################

def test_trim():
    TRIMMED = FSA(Real)

    TRIMMED.add_arc(State(0), Sym('b'), State(1), w=Real(0.1))


    TRIMMED.add_arc(State(1), Sym('b'), State(1), w=Real(0.2))
    TRIMMED.add_arc(State(1), Sym('a'), State(2), w=Real(0.3))
    TRIMMED.add_arc(State(1), Sym('a'), State(3), w=Real(0.4))


    TRIMMED.add_arc(State(2), Sym('b'), State(3), w=Real(0.5))

    TRIMMED.set_I(State(0), w=Real(1.0))
    TRIMMED.add_F(State(3), w=Real(0.6))

    assert compare_fsas(TRIMMED, NOT_TRIMMED_FSA.trim())


##########################
##### Testing union algorithm
##########################

def test_union():
    with open(f"{hw_path}/union_fsas.pkl", 'rb') as f:
        union_fsas = pickle.load(f)
    
    middle = int(len(fsas)/2)
    for left_fsa, right_fsa, union_fsa in zip(fsas[:middle], fsas[middle:], union_fsas):
        assert compare_fsas(union_fsa, left_fsa.union(right_fsa))


def test_union_example():
    UNION = FSA(Real)

    UNION.add_arc(PairState(1,2), Sym('a'), PairState(1,0), w=Real(0.128))
    UNION.add_arc(PairState(1,2), Sym('a'), PairState(1,2), w=Real(0.088))
    UNION.add_arc(PairState(1,2), Sym('b'), PairState(1,1), w=Real(0.024))

    UNION.add_arc(PairState(2,1), Sym('b'), PairState(2,0), w=Real(0.125))
    UNION.add_arc(PairState(2,1), Sym('b'), PairState(2,1), w=Real(0.007))
    UNION.add_arc(PairState(2,1), Sym('b'), PairState(2,2), w=Real(0.074))
    UNION.add_arc(PairState(2,1), Sym('a'), PairState(2,2), w=Real(0.047))

    UNION.add_arc(PairState(1,1), Sym('a'), PairState(1,0), w=Real(0.125))
    UNION.add_arc(PairState(1,1), Sym('a'), PairState(1,2), w=Real(0.026))
    UNION.add_arc(PairState(1,1), Sym('b'), PairState(1,0), w=Real(0.151))

    UNION.add_arc(PairState(2,0), Sym('b'), PairState(2,0), w=Real(0.147))
    UNION.add_arc(PairState(2,0), Sym('b'), PairState(2,1), w=Real(0.136))
    UNION.add_arc(PairState(2,0), Sym('b'), PairState(2,2), w=Real(0.025))
    UNION.add_arc(PairState(2,0), Sym('a'), PairState(2,1), w=Real(0.076))
    UNION.add_arc(PairState(2,0), Sym('a'), PairState(2,2), w=Real(0.159))

    UNION.add_arc(PairState(2,2), Sym('a'), PairState(2,0), w=Real(0.019))
    UNION.add_arc(PairState(2,2), Sym('a'), PairState(2,2), w=Real(0.084))
    UNION.add_arc(PairState(2,2), Sym('b'), PairState(2,0), w=Real(0.15))

    UNION.add_arc(PairState(1,0), Sym('a'), PairState(1,0), w=Real(0.043))
    UNION.add_arc(PairState(1,0), Sym('a'), PairState(1,1), w=Real(0.147))
    UNION.add_arc(PairState(1,0), Sym('b'), PairState(1,2), w=Real(0.108))


    UNION.set_I(PairState(1,0), w=Real(0.078))
    UNION.set_I(PairState(2,0), w=Real(0.141))

    UNION.add_F(PairState(1,2), w=Real(0.156))
    UNION.add_F(PairState(2,2), w=Real(0.062))

    union = FSA1.union(FSA2)

    assert compare_fsas(UNION,union)

##########################
##### Testing concatenate algorithm
##########################

def test_concatenate():
    with open(f"{hw_path}/concat_fsas.pkl", 'rb') as f:
        concat_fsas = pickle.load(f)
    
    middle = int(len(fsas)/2)
    for left_fsa, right_fsa, concat_fsa in zip(fsas[:middle], fsas[middle:], concat_fsas):
        assert compare_fsas(concat_fsa, left_fsa.concatenate(right_fsa))

def test_concatenate_example():
    CONCAT = FSA(Real)

    CONCAT.add_arc(PairState(1,2), Sym('a'), PairState(1,0), w=Real(0.128))
    CONCAT.add_arc(PairState(1,2), Sym('a'), PairState(1,2), w=Real(0.088))
    CONCAT.add_arc(PairState(1,2), Sym('b'), PairState(1,1), w=Real(0.024))
    CONCAT.add_arc(PairState(1,2), ε, PairState(2,0), w=Real(0.021996))


    CONCAT.add_arc(PairState(2,1), Sym('b'), PairState(2,0), w=Real(0.125))
    CONCAT.add_arc(PairState(2,1), Sym('b'), PairState(2,1), w=Real(0.007))
    CONCAT.add_arc(PairState(2,1), Sym('b'), PairState(2,2), w=Real(0.074))
    CONCAT.add_arc(PairState(2,1), Sym('a'), PairState(2,2), w=Real(0.047))

    CONCAT.add_arc(PairState(1,1), Sym('a'), PairState(1,0), w=Real(0.125))
    CONCAT.add_arc(PairState(1,1), Sym('a'), PairState(1,2), w=Real(0.026))
    CONCAT.add_arc(PairState(1,1), Sym('b'), PairState(1,0), w=Real(0.151))

    CONCAT.add_arc(PairState(2,0), Sym('b'), PairState(2,0), w=Real(0.147))
    CONCAT.add_arc(PairState(2,0), Sym('b'), PairState(2,1), w=Real(0.136))
    CONCAT.add_arc(PairState(2,0), Sym('b'), PairState(2,2), w=Real(0.025))
    CONCAT.add_arc(PairState(2,0), Sym('a'), PairState(2,1), w=Real(0.076))
    CONCAT.add_arc(PairState(2,0), Sym('a'), PairState(2,2), w=Real(0.159))

    CONCAT.add_arc(PairState(2,2), Sym('a'), PairState(2,0), w=Real(0.019))
    CONCAT.add_arc(PairState(2,2), Sym('a'), PairState(2,2), w=Real(0.084))
    CONCAT.add_arc(PairState(2,2), Sym('b'), PairState(2,0), w=Real(0.15))

    CONCAT.add_arc(PairState(1,0), Sym('a'), PairState(1,0), w=Real(0.043))
    CONCAT.add_arc(PairState(1,0), Sym('a'), PairState(1,1), w=Real(0.147))
    CONCAT.add_arc(PairState(1,0), Sym('b'), PairState(1,2), w=Real(0.108))


    CONCAT.set_I(PairState(1,0), w=Real(0.078))

    CONCAT.add_F(PairState(2,2), w=Real(0.062))

    concat = FSA1.concatenate(FSA2)
    
    assert compare_fsas(CONCAT,concat)

##########################
##### Testing Kleene closure algorithm
##########################


def test_closure():
    with open(f"{hw_path}/kleene_fsas.pkl", 'rb') as f:
        kleene_fsas = pickle.load(f)
    
    for fsa, kleene in zip(fsas, kleene_fsas):
        assert compare_fsas(kleene, fsa.kleene_closure())

def test_closure_example():
    KLEENE = FSA(Real)

    KLEENE.add_arc(State(0), Sym('a'), State(0), w=Real(0.043))
    KLEENE.add_arc(State(0), Sym('a'), State(1), w=Real(0.147))
    KLEENE.add_arc(State(0), Sym('b'), State(2), w=Real(0.108))
    KLEENE.add_arc(State(0), ε, State(2), w=Real(1.0))

    KLEENE.add_arc(State(1), Sym('a'), State(0), w=Real(0.125))
    KLEENE.add_arc(State(1), Sym('a'), State(2), w=Real(0.026))
    KLEENE.add_arc(State(1), Sym('b'), State(0), w=Real(0.151))

    KLEENE.add_arc(State(2), Sym('a'), State(0), w=Real(0.128))
    KLEENE.add_arc(State(2), Sym('a'), State(2), w=Real(0.088))
    KLEENE.add_arc(State(2), Sym('b'), State(1), w=Real(0.024))
    KLEENE.add_arc(State(2), ε, State(5), w=Real(0.156))
    KLEENE.add_arc(State(2), ε, State(0), w=Real(1.0))

    KLEENE.add_arc(State(4), ε, State(0), w=Real(0.078))
    KLEENE.add_arc(State(5), ε, State(4), w=Real(1.0))


    KLEENE.set_I(State(4), w=Real(1.0))
    KLEENE.add_F(State(5), w=Real(1.0))

    kleene = FSA1.kleene_closure()
    assert compare_fsas(KLEENE,kleene)