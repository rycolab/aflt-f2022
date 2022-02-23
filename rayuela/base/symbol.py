class Sym:

	def __init__(self, sym):
		self.sym = sym

	def __str__(self):
		return str(self.sym)

	def __repr__(self):
		return str(self.sym)

	def __hash__(self):
		return hash(self.sym)

	def __eq__(self, other):
		return isinstance(other, Sym) and self.sym == other.sym

ε = Sym("ε")
ε_1 = Sym("ε_1")
ε_2 = Sym("ε_2")
