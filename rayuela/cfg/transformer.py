import itertools as it
from itertools import chain, combinations

from rayuela.base.semiring import Boolean, Real, Derivation
from rayuela.base.symbol import Sym, ε

from rayuela.fsa.state import State
from rayuela.fsa.pathsum import Pathsum

from rayuela.cfg.nonterminal import NT, S, Slash, Other
from rayuela.cfg.production import Production
from rayuela.cfg.cfg import CFG
from rayuela.cfg.treesum import Treesum
from rayuela.cfg.misc import *


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


class Transformer:

    def __init__(self):
        self.counter = 0

    def _gen_nt(self):
        self.counter += 1
        return NT(f"@{self.counter}")

    def booleanize(self, cfg):
        one = Boolean(True)
        ncfg = CFG(R=Boolean)
        ncfg.S = cfg.S
        for p, w in cfg.P:
            if w != cfg.R.zero:
                ncfg.add(one, p.head, *p.body)
        return ncfg

    def _fold(self, cfg, p, w, I):

        # basic sanity checks
        for (i, j) in I:
            assert i >= 0 and j >= i and j < len(p.body)

        # new productions
        P, heads = [], []
        for (i, j) in I:
            head = self._gen_nt()
            heads.append(head)
            body = p.body[i:j+1]
            P.append(((head, body), cfg.R.one))

        # new "head" production
        body = tuple()
        start = 0
        for (end, n), head in zip(I, heads):
            body += p.body[start:end] + (head,)
            start = n+1
        body += p.body[start:]
        P.append(((p.head, body), w))

        return P

    def fold(self, cfg, p, w, I):
        ncfg = cfg.spawn()
        add = ncfg.add

        for (q, w) in cfg.P:
            if p != q:
                add(w, q.head, *q.body)

        for (head, body), w, in self._fold(cfg, p, w, I):
            add(w, head, *body)

        ncfg.make_unary_fsa()
        return ncfg

    def cnf(self, cfg):

        # remove terminals
        ncfg = self.separate_terminals(cfg)

        # remove nullary rules
        ncfg = self.nullaryremove(ncfg)

        # remove unary rules
        ncfg = self.unaryremove(ncfg)

        # binarize
        ncfg = self.binarize(ncfg)

        return ncfg.trim()

    def unaryremove(self, cfg) -> CFG:
        # Assignment 6
        raise NotImplementedError

    def nullaryremove(self, cfg) -> CFG:
        # Assignment 6
        raise NotImplementedError

    def separate_terminals(self, cfg) -> CFG:
        # Assignment 7
        raise NotImplementedError

    def binarize(self, cfg) -> CFG:
        # Assignment 7
        raise NotImplementedError

