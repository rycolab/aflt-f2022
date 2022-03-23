from rayuela.fsa.fsa import FSA
import pickle

# TODO: 
# - Examples
# - Edge cases

with open("tests/pickles/fsas.pkl", 'rb') as f:
    fsas = pickle.load(f)



def test_deterministic():
    for fsa in fsas:
        assert fsa.deterministic == True


def test_pushed():
    with open("tests/pickles/pushed_fsas.pkl", 'rb') as f:
        pushed_fsas = pickle.load(f)
    with open("tests/pickles/pushed_results.pkl", 'rb') as f:
        pushed_results = pickle.load(f)

    for gt_fsa, result in zip(pushed_fsas, pushed_results):
        assert gt_fsa.pushed == result
    

def test_reverse():
    
    with open("tests/pickles/reversed_fsas_ascii.pkl", 'rb') as f:
        reversed_asciis = pickle.load(f)
    
    for fsa, rfsa in zip(fsas, reversed_asciis):
        assert fsa.reverse().__str__() == rfsa

def test_accessible():
    
    with open("tests/pickles/accessible_states.pkl", 'rb') as f:
        accessible_states_fsas = pickle.load(f)
    
    for fsa, accessible_states in zip(fsas, accessible_states_fsas):
        assert fsa.accesible() == accessible_states

def test_coaccessible():
    
    with open("tests/pickles/coaccessible_states.pkl", 'rb') as f:
        coaccessible_states_fsas = pickle.load(f)
    
    for fsa, coaccessible_states in zip(fsas, coaccessible_states_fsas):
        assert fsa.coaccesible() == coaccessible_states

