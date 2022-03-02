import numpy as np
from fractions import Fraction

from collections import defaultdict as dd

from rayuela.base.misc import lcp

# base code from https://github.com/timvieira/hypergraphs/blob/master/hypergraphs/semirings/boolean.py
class Semiring:

    zero = None
    one = None
    idempotent = False

    def __init__(self, score):
        self.score = score

    @classmethod
    def zeros(cls, N, M):
        return np.full((N, M), cls.zero)

    @classmethod
    def chart(cls, default=None):
        if default is None:
            default = cls.zero
        return dd(lambda : default)

    @classmethod
    def diag(cls, N):
        W = cls.zeros(N, N)
        for n in range(N):
            W[n, n] = cls.one

        return W       

    def __add__(self, other):
        raise NotImplementedError

    def __mul__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        return self.score == other.score

    def __hash__(self):
        return hash(self.score)


class Derivation(Semiring):

    def __init__(self, score):
        super().__init__(score)

    def __add__(self, other):
        return Derivation(self.score.union(other.score))

    def __mul__(self, other):
        # TODO: add special cases
        return Derivation(set([x + y for x in self.score for y in other.score]))

    def __eq__(self, other):
        return self.score == other.score

    def __repr__(self):
        return f'Derivation({self.score})'

    def __hash__(self):
        return hash(self.score)

Derivation.zero = Derivation(set([]))
Derivation.one = Derivation(set([tuple()]))
Derivation.idempotent = False


class KBest(Semiring):

    def __init__(self, score):
        super().__init__(score)

    def __add__(self, other):
        return KBest(self.score.union(other.score))

    def __mul__(self, other):
        # TODO: add special cases
        return KBest(set([x + y for x in self.score for y in other.score]))

    def __eq__(self, other):
        return self.score == other.score

    def __repr__(self):
        return f'KBest({self.score})'

    def __hash__(self):
        return hash(self.score)

KBest.zero = Derivation(set([]))
KBest.one = Derivation(set([tuple()]))
KBest.idempotent = False


class Free(Semiring):

    def __init__(self, score):
        super().__init__(score)

    def star(self):
        return "("+self.score+")^*"

    def __add__(self, other):
        if other is self.zero: return self
        if self is self.zero: return other
        return Free(self.score + " + " + other.score)

    def __mul__(self, other):
        if other is self.one: return self
        if self is self.one: return other
        if other is self.zero: return self.zero
        if self is self.zero: return self.zero
        return Free(self.score + other.score)

    def __eq__(self, other):
        return self.score == other.score

    def __repr__(self):
        return f'Free({self.score})'

    def __hash__(self):
        return hash(self.score)

Free.zero = Free("∞")
Free.one = Free("")
Free.idempotent = False

class Count(Semiring):

    def __init__(self, score):
        super().__init__(score)

    def __add__(self, other):
        if other is self.zero: return self
        if self is self.zero: return other
        return Count(self.score + other.score)

    def __mul__(self, other):
        if other is self.one: return self
        if self is self.one: return other
        if other is self.zero: return self.zero
        if self is self.zero: return self.zero
        return Count(self.score * other.score)

    def __eq__(self, other):
        return self.score == other.score

    def __repr__(self):
        return f'{self.score}'

    def __hash__(self):
        return hash(self.score)

    def __float__(self):
        return float(self.score)

Count.zero = Count(0)
Count.one = Count(1)
Count.idempotent = False


class Entropy(Semiring):

    def __init__(self, x, y):
        super().__init__((x, y))

    def __add__(self, other):
        if other is self.zero: return self
        if self is self.zero: return other
        return Entropy(self.score[0] + other.score[0], self.score[1] + other.score[1])

    def __mul__(self, other):
        if other is self.one: return self
        if self is self.one: return other
        if other is self.zero: return self.zero
        if self is self.zero: return self.zero
        return Entropy(self.score[0] * other.score[0], self.score[0] * other.score[1] + self.score[1] * other.score[0])

    def __eq__(self, other):
        return self.score == other.score

    def __repr__(self):
        return f'Entropy({self.score})'

    def __hash__(self):
        return hash(self.score)

Entropy.zero = Entropy(0.0, 0.0)
Entropy.one = Entropy(1.0, 0.0)
Entropy.idempotent = False



class String(Semiring):

    def __init__(self, score):
        super().__init__(score)

    def star(self):
        return String.one

    def __add__(self, other):
        if other is self.zero: return self
        if self is self.zero: return other
        return String(lcp(self.score, other.score))

    def __mul__(self, other):
        if other is self.one: return self
        if self is self.one: return other
        if other is self.zero: return self.zero
        if self is self.zero: return self.zero
        return String(self.score + other.score)

    def __truediv__(self, other):
        prefix = lcp(self.score, other.score)
        return String(self.score[len(prefix):])

    def __eq__(self, other):
        return self.score == other.score

    def __repr__(self):
        return f'{self.score}'

    def __hash__(self):
        return hash(self.score)

# unique "infinity" string
String.zero = String("∞")
# empty string
String.one = String("")
String.idempotent = False


class Boolean(Semiring):

    def __init__(self, score):
        super().__init__(score)

    def star(self):
        return Boolean.one

    def __add__(self, other):
        return Boolean(self.score or other.score)

    def __mul__(self, other):
        if other.score is self.one: return self.score
        if self.score is self.one: return other.score
        if other.score is self.zero: return self.zero
        if self.score is self.zero: return self.zero
        return Boolean(other.score and self.score)

    def __eq__(self, other):
        return self.score == other.score

    def __lt__(self, other):
        return self.score < other.score

    def __repr__(self):
        return f'{self.score}'

    def __str__(self):
        return str(self.score)

    def __hash__(self):
        return hash(self.score)

Boolean.zero = Boolean(False)
Boolean.one = Boolean(True)
Boolean.idempotent = True


class MaxPlus(Semiring):

    def __init__(self, score):
        super().__init__(score)

    def star(self):
        return self.one

    def __float__(self):
        return float(self.score)

    def __add__(self, other):
        return MaxPlus(max(self.score, other.score))

    def __mul__(self, other):
        if other is self.one: return self
        if self is self.one: return other
        if other is self.zero: return self.zero
        if self is self.zero: return self.zero
        return MaxPlus(self.score + other.score)

    def __invert__(self):
        return MaxPlus(-self.score)

    def __truediv__(self, other):
        return MaxPlus(self.score - other.score)

    def __lt__(self, other):
        return self.score < other.score

    def __repr__(self):
        return f'MaxPlus({self.score})'

MaxPlus.zero = MaxPlus(float('-inf'))
MaxPlus.one = MaxPlus(0.0)
MaxPlus.idempotent = True
MaxPlus.superior = True
MaxPlus.cancellative = True


class Tropical(Semiring):

    def __init__(self, score):
        self.score = score

    def star(self):
        return self.one

    def __float__(self):
        return float(self.score)

    def __int__(self):
        return int(self.score)

    def __add__(self, other):
        return Tropical(min(self.score, other.score))

    def __mul__(self, other):
        if other is self.one: return self
        if self is self.one: return other
        if other is self.zero: return self.zero
        if self is self.zero: return self.zero
        return Tropical(self.score + other.score)

    def __invert__(self):
        return Tropical(-self.score)

    def __truediv__(self, other):
        return Tropical(self.score - other.score)

    def __lt__(self, other):
        return self.score < other.score

    def __repr__(self):
        return f'Tropical({self.score})'

    def __str__(self):
        return str(self.score)
        

Tropical.zero = Tropical(float('inf'))
Tropical.one = Tropical(0.0)
Tropical.idempotent = True
Tropical.superior = True
Tropical.cancellative = True


class Rational(Semiring):

    def __init__(self, score):
        self.score = Fraction(score)

    def star(self):
        return Rational(Fraction('1')/(Fraction('1')-self.score))

    def __float__(self):
        return float(self.score)

    def __add__(self, other):
        return Rational(self.score +  other.score)

    def __mul__(self, other):
        if other is self.one: return self
        if self is self.one: return other
        if other is self.zero: return self.zero
        if self is self.zero: return self.zero
        return Real(self.score * other.score)

    def __invert__(self):
        return Rational(1.0/self.score)

    def __truediv__(self, other):
        return Rational(self.score / other.score)

    def __eq__(self, other):
        return np.allclose(float(self.score), float(other.score))

    def __lt__(self, other):
        return self.score < other.score

    def __repr__(self):
        #return f'Real({self.score})'
        return f'{self.score}'

    # TODO: find out why this wasn't inherited
    def __hash__(self):
        return hash(self.score)


Rational.zero = Rational(Fraction('0'))
Rational.one = Rational(Fraction('1'))
Rational.idempotent = False
Rational.cancellative = True


class Real(Semiring):

    def __init__(self, score):
        # TODO: this is hack to deal with the fact
        # that we have to hash weights
        self.score = score

    def star(self):
        return Real(1.0/(1.0-self.score))

    def __float__(self):
        return float(self.score)

    def __add__(self, other):
        return Real(self.score +  other.score)

    def __mul__(self, other):
        if other is self.one: return self
        if self is self.one: return other
        if other is self.zero: return self.zero
        if self is self.zero: return self.zero
        return Real(self.score * other.score)

    def __invert__(self):
        return Real(1.0/self.score)

    def __truediv__(self, other):
        return Real(self.score / other.score)

    def __lt__(self, other):
        return self.score < other.score

    def __repr__(self):
        #return f'Real({self.score})'
        return f'{round(self.score, 15)}'

    def __eq__(self, other):
        #return float(self.score) == float(other.score)
        return np.allclose(float(self.score), float(other.score), atol=1e-2)

    # TODO: find out why this wasn't inherited
    def __hash__(self):
        return hash(self.score)

Real.zero = Real(0.0)
Real.one = Real(1.0)
Real.idempotent = False
Real.cancellative = True

class Integer(Semiring):

    def __init__(self, score):
        # TODO: this is hack to deal with the fact
        # that we have to hash weights
        self.score = score

    def __float__(self):
        return float(self.score)

    def __add__(self, other):
        return Integer(self.score +  other.score)

    def __mul__(self, other):
        if other is self.one: return self
        if self is self.one: return other
        if other is self.zero: return self.zero
        if self is self.zero: return self.zero
        return Integer(self.score * other.score)

    def __lt__(self, other):
        return self.score < other.score

    def __repr__(self):
        return f'Integer({self.score})'

    def __eq__(self, other):
        return float(self.score) == float(other.score)

    def __hash__(self):
        return hash(self.score)

Integer.zero = Integer(0)
Integer.one = Integer(1)
Integer.idempotent = False
Integer.cancellative = True

def vector_semiring_builder(semiring, N):

    class VectorSemiring(Semiring):
        def __init__(self, x):
            super().__init__(x)
        
        def star(self):
            raise NotImplemented
        
        def __add__(self, other):
            return VectorSemiring(self.score + other.score)

        def __mul__(self, other):
            return VectorSemiring(self.score * other.score)

        def __eq__(self, other):
            return self.score == other.score

        def __repr__(self):
            return f'Vector({self.score})'

        def __hash__(self):
            return hash(self.score)
        
    VectorSemiring.zero = VectorSemiring(np.full(N, semiring.zero))
    VectorSemiring.one = VectorSemiring(np.full(N, semiring.one))
    VectorSemiring.idempotent = semiring.idempotent
        
    return VectorSemiring


class ProductSemiring(Semiring):
    def __init__(self, x, y):
        super().__init__((x, y))

    def star(self):
        raise NotImplemented

    def __add__(self, other):
        w1, w2 = self.score[0], other.score[0]
        v1, v2 = self.score[1], other.score[1]
        return ProductSemiring(w1 + w2, v1 + v2)

    def __mul__(self, other):
        w1, w2 = self.score[0], other.score[0]
        v1, v2 = self.score[1], other.score[1]
        return ProductSemiring(w1 * w2, v1 * v2)

    def __eq__(self, other):
        return self.score == other.score

    def __repr__(self):
        if isinstance(self.score[0], String):
            # the imporant special case of encoding transducers
            if len(self.score[0].score) > 0:
                return f'{self.score[0]} / {self.score[1]}'
            else:
                return f'{self.score[1]}'
        return f'〈{self.score[0]}, {self.score[1]}〉'

    def __hash__(self):
        return hash(self.score)


def product_semiring_builder(semiring1, semiring2):

    ProductSemiring.zero = ProductSemiring(semiring1.zero, semiring2.zero)
    ProductSemiring.one = ProductSemiring(semiring1.one, semiring2.one)
    ProductSemiring.idempotent = semiring1.idempotent and semiring2.idempotent

    return ProductSemiring


def expectation_semiring_builder(semiring1, semiring2):

    class ExpectationSemiring(Semiring):
        def __init__(self, x, y):
            super().__init__((x, y))
        
        def star(self):
            raise NotImplemented
        
        def __add__(self, other):
            w1, w2 = self.score[0], other.score[0]
            v1, v2 = self.score[1], other.score[1]
            return ExpectationSemiring(w1 + w2, v1 + v2)

        def __mul__(self, other):
            w1, w2 = self.score[0], other.score[0]
            v1, v2 = self.score[1], other.score[1]     
            return ExpectationSemiring(w1 * w2, w1 * v2 + w2 * v1)

        def __eq__(self, other):
            return self.score == other.score

        def __repr__(self):
            return f'Expect({self.score})'

        def __hash__(self):
            return hash(self.score)
        
    ExpectationSemiring.zero = ExpectationSemiring(semiring1.zero, semiring2.zero)
    ExpectationSemiring.one = ExpectationSemiring(semiring1.one, semiring2.one)
    ExpectationSemiring.idempotent = semiring1.idempotent and semiring2.idempotent
        
    return ExpectationSemiring
