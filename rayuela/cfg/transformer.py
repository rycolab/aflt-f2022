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

def unary(p):
    # X → Y
    if len(p.body) == 1 and isinstance(p.body[0], NT):
        return True
    return False

def preterminal(p):
    # X → a
    (head, body) = p
    if len(body) == 1 and isinstance(p.body[0], Sym):
        return True
    return False

def binarized(p):
    # X → a
    (head, body) = p
    if len(body) == 2 and isinstance(p.body[0], NT) and isinstance(p.body[1], NT):
        return True
    return False


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

