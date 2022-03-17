from collections import defaultdict as dd
from itertools import chain, product
from sys import float_repr_style
from frozendict import frozendict

from rayuela.base.symbol import ε
from rayuela.fsa.state import MinimizeState, PowerState
from rayuela.fsa.pathsum import Pathsum, Strategy


class Transformer:

    def trim(fsa):
        raise NotImplementedError

    def powerarcs(fsa, powerstate):
        """
        This helper method group outgoing arcs for determinization.
        """
        zero, one = fsa.R.zero, fsa.R.one
        sym2arc, sym2sum = dd(list), fsa.R.chart()

        for s in powerstate.idx:
            for sym, t, w in fsa.arcs(s):
                sym2arc[sym].append((s, sym, t, w))
                sym2sum[sym] += powerstate.weights[s] * w

        for sym, arcs in sym2arc.items():
            weights = fsa.R.chart()
            for (s, sym, t, w) in arcs:
                weights[t] += powerstate.weights[s] * w / sym2sum[sym]

            yield sym, PowerState([t for (_, _, t, _) in arcs], weights), sym2sum[sym]

    def push(fsa):
        raise NotImplementedError

    def _push(fsa, V):
        raise NotImplementedError

    def _eps_partition(fsa):
        """ partition fsa into two (one with eps arcs and one with all others) """

        E = fsa.spawn()
        N = fsa.spawn(keep_init=True, keep_final=True)

        for q in fsa.Q:
            E.add_state(q)
            N.add_state(q)

        for i in fsa.Q:
            for a, j, w in fsa.arcs(i):
                if a == ε:
                    E.add_arc(i, a, j, w)
                else:
                    N.add_arc(i, a, j, w)

        return N, E

    def epsremoval(fsa):

        # note that N keeps same initial and final weights
        N, E = Transformer._eps_partition(fsa)
        W = Pathsum(E).lehmann(zero=False)

        for i in fsa.Q:
            for a, j, w in fsa.arcs(i, no_eps=True):
                for k in fsa.Q:
                    N.add_arc(i, a, k, w * W[j, k])

        # additional initial states
        for i, j in product(fsa.Q, repeat=2):
            N.add_I(j, fsa.λ[i] * W[i, j])


        return N

