from frozendict import frozendict

from rayuela.base.semiring import Boolean
from rayuela.base.symbol import Sym, ε

from rayuela.fsa.fsa import FSA
from rayuela.fsa.state import State


class FST(FSA):

	def __init__(self, R=Boolean):

		# DEFINITION
		# A weighted finite-state transducer is a 8-tuple <Σ, Δ, Q, F, I, δ, λ, ρ> where
		# • Σ is an alphabet of symbols;
		# • Δ is an alphabet of symbols;
		# • Q is a finite set of states;
		# • I ⊆ Q is a set of initial states;
		# • F ⊆ Q is a set of final states;
		# • δ is a finite relation Q × Σ × Δ × Q × R;
		# • λ is an initial weight function;
		# • ρ is a final weight function.

		# NOTATION CONVENTIONS
		# • single states (elements of Q) are denoted q
		# • multiple states not in sequence are denoted, p, q, r, ...
		# • multiple states in sequence are denoted i, j, k, ...
		# • symbols (elements of Σ and Δ) are denoted lowercase a, b, c, ...
		# • single weights (elements of R) are denoted w
		# • multiple weights (elements of R) are denoted u, v, w, ...

		super().__init__(R=R)

		# alphabet of output symbols
		self.Delta = set()

	def add_arc(self, i, a, b, j, w=None):
		if w is None: w = self.R.one

		if not isinstance(i, State): i = State(i)
		if not isinstance(j, State): j = State(j)
		if not isinstance(a, Sym): a = Sym(a)
		if not isinstance(a, Sym): b = Sym(b)
		if not isinstance(w, self.R): w = self.R(w)

		self.add_states([i, j])
		self.Sigma.add(a)
		self.Delta.add(b)
		self.δ[i][(a, b)][j] += w

	def set_arc(self, i, a, b, j, w):
		self.add_states([i, j])
		self.Sigma.add(a)
		self.Delta.add(b)
		self.δ[i][a][j] = w

	def freeze(self):
		self.Sigma = frozenset(self.Sigma)
		self.Delta = frozenset(self.Delta)
		self.Q = frozenset(self.Q)
		self.δ = frozendict(self.δ)
		self.λ = frozendict(self.λ)
		self.ρ = frozendict(self.ρ)

	def arcs(self, i, no_eps=False):
		for ab, T in self.δ[i].items():
			if no_eps and ab == (ε, ε):
				continue
			for j, w in T.items():
				if w == self.R.zero:
					continue
				yield ab, j, w

	def accept(self, string1, string2):
		""" determines whether a string is in the language """
		# Requires composition
		raise NotImplementedError

	def top_compose(self, fst):
		# Homework 3 
		raise NotImplementedError

	def bottom_compose(self, fst):
		# Homework 3
		raise NotImplementedError
