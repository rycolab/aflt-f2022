import random
import string
import numpy as np
from fractions import Fraction

def spans(min, max, depth, span=()):
    for n in range(min+1, max):
        if depth == 0:
            yield span+(n,)
        else:
            for x in spans(n, max, depth-1, span+(n,)):
                yield x

def lcp(str1, str2):
    """ computes the longest common prefix """
    prefix = ""
    for n in range(min(len(str1), len(str2))):
        if str1[n] == str2[n]:
            prefix += str1[n]
        else:
            break
    return prefix


def symify(string):
    from rayuela.base.symbol import Sym
    return [Sym(x) for x in list(string)]


def straight(string, R, Sigma):
    from rayuela.base.symbol import Sym
    from rayuela.fsa.fsa import FSA
    from rayuela.fsa.state import State

    fsa = FSA(R=R)
    for i, x in enumerate(list(string)):
        fsa.add_arc(State(i), Sym(x), State(i+1), R.one)
    fsa.set_I(State(0), R.one)
    fsa.add_F(State(len(string)), R.one)

    return fsa


def _random_weight(semiring):
    from rayuela.base.semiring import Count, Integer, Real, Rational, Tropical, Boolean, MaxPlus, String

    if semiring is String:
        str_len = int(random.random() * 8 + 1)
        return semiring(''.join(
            random.choice(string.ascii_lowercase) for _ in range(str_len)))

    elif semiring is Boolean:
        return semiring(True)

    elif semiring is Real:
        return semiring(float(1.0/random.randint(5, 10)))

        #return semiring(round(random.random() / 5, 3))
        #return semiring(round(random.randint(1, 4)))

    elif semiring is Rational:
        #return semiring(Fraction(f"{random.randint(1, 5)}/{random.randint(1, 5)}"))
        #return semiring(Fraction(f"1/{random.randint(2, 5)}"))
        return semiring(Fraction(f"{random.randint(1, 5)}/1"))

    elif semiring is Tropical:
        return semiring(random.randint(0, 50))

    elif semiring is Integer:
        return semiring(random.randint(1, 10))

    elif semiring is MaxPlus:
        return semiring(random.randint(-10, -1))

    elif semiring is Count:
        return semiring(1.0)

def random_weight_negative(semiring):
    from rayuela.base.semiring import Real, Rational, Tropical, Boolean, MaxPlus, String

    if semiring is Tropical:
        return semiring(random.randint(-50, 50))
    else:
        raise AssertionError("Unsupported Semiring")


def epsilon_filter(a1, a2, q3):
    """
    Filter for composition with epsilon transitions 
    """
    from rayuela.fsa.state import State
    from rayuela.base.symbol import ε_1, ε_2
    if a1 == a2 and a1 not in [ε_1, ε_2]:
        return State('0')
    elif a1 == ε_2 and a2 == ε_1 and q3 == State('0'):
        return State('0')
    elif a1 == ε_1 and a2 == ε_1 and q3 != State('2'):
        return State('1')
    elif a1 == ε_2 and a2 == ε_2 and q3 != State('1'):
        return State('2')
    else:
        return State('⊥')

def is_pathsum_positive(fsa):
    from rayuela.fsa.fsa import FSA
    assert isinstance(fsa, FSA)
    
    return fsa.pathsum() > fsa.R.zero

def compare_fsas(original_fsa, student_fsa) -> bool:
    from rayuela.fsa.fsa import FSA
    assert isinstance(original_fsa, FSA)
    assert isinstance(student_fsa, FSA)

    if is_pathsum_positive(original_fsa):
        return np.allclose(float(original_fsa.pathsum()), float(student_fsa.pathsum()), atol=1e-3)
    # Skip non-convergent pathsums
    return True


def compare_charts(chart1, chart2) -> "tuple[bool,bool]":
    # Assert both have the same keys
    same_keys =  set(chart1.keys()) == set(chart2.keys())

    # Assert all values are similar
    same_values = False
    if same_keys:
        same_values = all([np.allclose(float(chart1[key]),float(chart2[key]), atol=1e-3) for key in chart1.keys()])

    return same_keys and same_values

def compare_chart(semiring, chart1, chart2):
    for item in set(chart1.keys()).intersection(set(chart2.keys())):
        if np.allclose(float(chart1[item]), float(chart2[item]), atol=1e-2):
            print("\t".join([colors.green % str(item), str(chart1[item])]))
        else:
            print("\t".join([colors.light.red % str(item), str(chart1[item]), str(chart2[item])]))
    return
    for item in chart2:
        if item not in chart1:
            if chart2[item] != semiring.zero:
                print("\t".join([colors.yellow % str(item), str(chart2[item])]))


def ansi(color=None, light=None, bg=3):
    return '\x1b[%s;%s%sm' % (light, bg, color)

_reset = '\x1b[0m'


def colorstring(s, c):
    return c + s + _reset


class colors:
    black, red, green, yellow, blue, magenta, cyan, white = \
        [colorstring('%s', ansi(c, 0)) for c in range(8)]

    class light:
        black, red, green, yellow, blue, magenta, cyan, white = \
            [colorstring('%s', ansi(c, 1)) for c in range(8)]

    class dark:
        black, red, green, yellow, blue, magenta, cyan, white = \
            [colorstring('%s', ansi(c, 2)) for c in range(8)]

    class bg:
        black, red, green, yellow, blue, magenta, cyan, white = \
            [colorstring('%s', ansi(c, 0, bg=4)) for c in range(8)]

    normal = '\x1b[0m%s\x1b[0m'
    bold = '\x1b[1m%s\x1b[0m'
    italic = "\x1b[3m%s\x1b[0m"
    underline = "\x1b[4m%s\x1b[0m"
    strike = "\x1b[9m%s\x1b[0m"
    #overline = lambda x: (u''.join(unicode(c) + u'\u0305' for c in unicode(x))).encode('utf-8')

    leftarrow = '←'
    rightarrow = '→'
    reset = _reset