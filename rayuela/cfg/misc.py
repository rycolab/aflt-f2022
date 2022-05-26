from itertools import chain, combinations
from rayuela.base.symbol import Sym, ε
from rayuela.cfg.nonterminal import NT, S


# TODO: move to a misc file
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

def nullary(p):
    # ε
    head, body = p
    if head == S:
        # When head is S we allow the ε in the body
        return False
    for elem in body:
        if elem == ε:
            return True
    return False

def separated(p):
    (head, body) = p
    if isinstance(body[0], NT):
        r = all([isinstance(elem, NT) for elem in body])
    elif isinstance(body[0], Sym):
        r = all([isinstance(elem, Sym) for elem in body])
    else:
        raise ValueError("All body elements are neither 'NT' nor 'Sym'")
    return r


# TODO move to misc
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))