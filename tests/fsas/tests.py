from rayuela.fsa.fsa import FSA
import pickle

with open("tests/fsas/fsas.pkl", 'rb') as f:
    fsas = pickle.load(f)

with open("tests/fsas/pushed_fsas.pkl", 'rb') as f:
    gt_pushed_fsas = pickle.load(f)

def test_deterministic():
    for fsa in fsas:
        assert fsa.deterministic == True


def test_pushed():
    pushed_fsas = [fsa.push() for fsa in fsas]
    for gt_fsa, pushed_fsa in zip(gt_pushed_fsas, pushed_fsas):
        assert pushed_fsa.pushed == True
        assert gt_fsa.__str__() == pushed_fsa.__str__()
    

def test_reverse():
    for fsa in fsas:
        assert fsa.reverse() == "Reverse"