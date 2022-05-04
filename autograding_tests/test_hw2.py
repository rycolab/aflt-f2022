from rayuela.fsa.fsa import FSA
import pickle
from rayuela.base.semiring import Tropical, Real
from rayuela.fsa.state import PairState, State
from rayuela.base.symbol import Sym, ε
import numpy as np
from rayuela.fsa.pathsum import Pathsum, Strategy
from rayuela.base.misc import compare_charts, compare_fsas

pickles_path = "autograding_tests/pickles"
hw_path = pickles_path + "/hw2"

with open(f"{pickles_path}/fsas.pkl", 'rb') as f:
    fsas = pickle.load(f)


def test_viterbi_fwd():
    
    with open(f"{hw_path}/hw2_viterbi_fwd.pkl", 'rb') as f:
        α = pickle.load(f)
    
    # Viterbi needs acyclic fsa
    acyclic_fsas = [fsa for fsa in fsas if fsa.acyclic]
    for fsa, a in zip(acyclic_fsas, α):
        alpha = Pathsum(fsa).forward(Strategy.VITERBI)

        assert compare_charts(a,alpha)

def test_edge_marginals():
    
    with open(f"{hw_path}/hw2_marginals.pkl", 'rb') as f:
        marginals = pickle.load(f)
    
    # Viterbi needs acyclic fsa
    acyclic_fsas = [fsa for fsa in fsas if fsa.acyclic]
    for fsa, marginal in zip(acyclic_fsas, marginals):
        computed_marginals = fsa.edge_marginals()
        
        #Assert both have the same qs
        assert set(computed_marginals.keys()) == set(marginal.keys())

        for q in marginal.keys():
            
            #Assert every state has the same labels
            assert set(computed_marginals[q].keys()) == set(marginal[q].keys()) 

            for a in marginal[q].keys():

                #Assert every label goes to the same states
                assert set(computed_marginals[q][a].keys()) == set(marginal[q][a].keys())

                for q_prima in marginal[q][a]:

                    #Assert alpha values are close enough
                    assert np.allclose(float(marginal[q][a][q_prima]),float(computed_marginals[q][a][q_prima]), atol=1e-3)


def test_coaccessible_intersection():

    left_fsas, right_fsas = fsas[:500], fsas[500:]

    for left, right in zip(left_fsas, right_fsas):
        intersected_fsas = left.intersect(right)
        coaccessible_intersected = left.coaccessible_intersection(right)

        #fsas have same pathsum
        assert compare_fsas(intersected_fsas, coaccessible_intersected)

        #only coaccesible states
        assert coaccessible_intersected.Q == coaccessible_intersected.coaccessible()