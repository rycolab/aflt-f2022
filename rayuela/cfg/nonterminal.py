from rayuela.base.symbol import Sym
class NT:

	def __init__(self, X, label=None, n=None):
		self._X = X
		self._label = label
		self.num = n

	@property
	def X(self):
		return self._X

	@property
	def label(self):
		return self._label

	def number(self):
		return

	def set_label(self, label):
		self._label = label

	def copy(self):
		return NT(self.X)

	def __truediv__(self, Y):
		return Slash(self, Y)

	def __invert__(self):
		return Other(self)

	def __repr__(self):
		if self.label is not None:
			return f'{self.label}'
		return f'{self.X}'

	def __hash__(self):
		return hash(self.X)

	def __eq__(self, other):
		return isinstance(other, NT) and self.X == other.X

S = NT("S")
bottom = NT("⊥")


class Triplet(NT):
	def __init__(self, p, X, q, label=None):
		super().__init__((p, X, q), label=None)
		self._p, self._X, self._q = p, X, q

	@property
	def p(self):
		return self._p

	@property
	def X(self):
		return self._X

	@property
	def q(self):
		return self._q

	def __hash__(self):
		return hash(self.X)

	def __eq__(self, other):
		return isinstance(other, Triplet) \
			and self.p == other.p \
			and self.X == other.X \
			and self.q == other.q

	def __repr__(self):
		if self.label is not None:
			return f'{self.label}'
		return f"[{self.p}, {self.X}, {self.q}]"


class Slash(NT):

	def __init__(self, Y, Z, label=None):
		assert isinstance(Z, NT) or isinstance(Z, Sym)
		super().__init__((Y, Z), label=None)
		self._Y, self._Z = Y, Z

	@property
	def Y(self):
		return self._Y

	@property
	def Z(self):
		return self._Z

	def __repr__(self):
		if self.label is not None:
			return f'{self.label}'
		return f"{self.Y}"+"/"+f"{self.Z}"


class Other(NT):

	def __init__(self, X, label=None):
		super().__init__(X, label=None)

	def __repr__(self):
		if self.label is not None:
			return f'{self.label}'
		return f"~{self.X}"

	def __hash__(self):
		return hash(self.X)

	def __eq__(self, other):
		return isinstance(other, Other) and self.X == other.X
