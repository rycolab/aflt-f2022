from rayuela.fsa.fsa import FSA
import pickle

with open("tests/fsas/fsas.pkl", 'rb') as f:
    fsas = pickle.load(f)



def test_deterministic():
    for fsa in fsas:
        assert fsa.deterministic == True


def test_pushed():
    with open("tests/fsas/pushed_fsas.pkl", 'rb') as f:
        pushed_fsas = pickle.load(f)
    with open("tests/fsas/pushed_results.pkl", 'rb') as f:
        pushed_results = pickle.load(f)

    for gt_fsa, result in zip(pushed_fsas, pushed_results):
        assert gt_fsa.pushed == result
    

def test_reverse():
    for fsa in fsas:
        assert fsa.reverse() == "Reverse"