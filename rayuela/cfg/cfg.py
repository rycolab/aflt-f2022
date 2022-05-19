import copy
from frozendict import frozendict
from itertools import product

from rayuela.base.semiring import Boolean
from rayuela.base.symbol import Sym, ε
from rayuela.base.misc import straight

from rayuela.fsa.fsa import FSA
from rayuela.fsa.state import State

from rayuela.cfg.exceptions import InvalidProduction
from rayuela.cfg.nonterminal import NT, S, Triplet
from rayuela.cfg.production import Production
from rayuela.cfg.treesum import Treesum

class CFG:

	def __init__(self, R=Boolean):

		# A weighted context-free grammar is a 5-tuple <R, Σ, V, P, S> where
		# • R is a semiring;
		# • Σ is an alphabet of terminal symbols;
		# • V is an alphabet of non-terminal symbols;
		# • P is a finite relation V × (Σ ∪ V)* × R;
		# • S ∈ V is a distinguished started symbol.

		# semiring
		self.R = R

		# alphabet
		self.Sigma = set([])

		# non-terminals
		self.V = set([S])

		# productions
		self._P = self.R.chart()

		# unique start symbol
		self.S = S

		# unary FSA
		self.unary_fsa = None

	@property
	def terminal(self):
		for p, w in self.P:
			(head, body) = p
			if len(body) == 1 and isinstance(body[0], Sym):
				yield p, w

	@property
	def unary(self):
		for p, w in self.P:
			(head, body) = p
			if len(body) == 1 and isinstance(body[0], NT):
				yield p, w

	@property
	def binary(self):
		for p, w in self.P:
			(head, body) = p
			if len(body) == 2 and isinstance(body[0], NT) \
				and isinstance(body[1], NT):
				yield p, w

	@property
	def size(self):
		size = 0
		for (_, body), _ in self.P:
			size+=len(body)+1
		return size

	@property
	def num_rules(self):
		return len(self._P)

	def w(self, p):
		return self._P[p]

	def spawn(self):
		return CFG(R=self.R)

	def make_unary_fsa(self):
		one = self.R.one
		fsa = FSA(R=self.R)

		# add a state for every non-terminal
		for X in self.V:
			fsa.add_state(State(X))

		# add arcs between every pair of unary rules
		for (head, body), w in self.unary:
			fsa.add_arc(State(body[0]), ε, State(head), w)

		# add initial and final weight one for every state
		for q in list(fsa.Q):
			fsa.set_I(q, one)
			fsa.set_F(q, one)

		self.unary_fsa = fsa

	def eps_partition(self):
		""" makes a new grammar can only generate epsilons """
		ecfg = self.spawn()
		ncfg = self.spawn()

		def has_terminal(body):
			for elem in body:
				if isinstance(elem, Sym) and elem != ε:
					return True
			return False

		for p, w in self.P:
			head, body = p
			if has_terminal(body):
				ncfg.add(w, head, *body)
			elif len(body) == 1 and body[0] == ε:
				ecfg.add(w, head, *body)
			else:
				ncfg.add(w, head, *body)
				ecfg.add(w, head, *body)

		return ecfg, ncfg

	@property
	def P(self):
		for p, w in self._P.items():
			yield p, w

	def P_byhead(self, X, unary=True):
		for p, w in self._P.items():
			if X == p.head:
				if not unary and len(p.body) == 1 and isinstance(p.body[0], NT):
					continue
				yield p, w

	def add(self, w, head, *body):
		if not isinstance(head, NT):
			raise InvalidProduction
		self.V.add(head)

		for elem in body:
			if isinstance(elem, NT):
				self.V.add(elem)
			elif isinstance(elem, Sym):
				self.Sigma.add(elem)
			else:
				raise InvalidProduction

		self._P[Production(head, body)] += w

	def get_productions(self):
		return self._P

	def freeze(self):
		self.Sigma = frozenset(self.Sigma)
		self.V = frozenset(self.V)
		self._P = frozendict(self._P)

	def copy(self):
		return copy.deepcopy(self)

	def fresh(self):
		ncfg = self.spawn()
		for p, w in self.P:
			nbody = []
			for elem in p.body:
				if isinstance(elem, NT):
					nbody.append(NT(str(elem)))
				elif isinstance(elem, Sym):
					nbody.append(elem)
			ncfg.add(w, NT(str(p.head)), *nbody)
		ncfg.make_unary_fsa()

		return ncfg

	def accessible(self):
		from rayuela.cfg.transformer import Transformer
		from rayuela.cfg.treesum import Treesum

		boo = Transformer().booleanize(self)
		A = set([])
		for item, v in Treesum(boo).backwardchain().items():
			if v != Boolean.zero:
				A.add(item)

		return A

	def coaccessible(self):
		from rayuela.cfg.transformer import Transformer
		from rayuela.cfg.treesum import Treesum

		boo = Transformer().booleanize(self)
		C = set([])

		for item, v in Treesum(boo).forwardchain().items():
			if v != Boolean.zero:
				C.add(item)

		return C

	def treesum(self):
		treesum = Treesum(self)
		return treesum.sum()

	def accept(self, s):
		from rayuela.cfg.transformer import Transformer
		s = straight(s, R=Boolean)
		ncfg = Transformer().booleanize(self)
		return ncfg.intersect_fsa(s).treesum()

	def trim(self):
		return self._trim()._trim()

	def cnf(self):
		from rayuela.cfg.transformer import Transformer
		return Transformer().cnf(self)

	def elim(self, p):
		from rayuela.cfg.transformer import Transformer
		return Transformer().elim(self, p)

	def unfold(self, p, i):
		from rayuela.cfg.transformer import Transformer
		return Transformer().unfold2(self, p, i)

	def removenullary(self):
		from rayuela.cfg.transformer import Transformer
		return Transformer().nullaryremove(self)

	def _trim(self):
		A, C = self.accessible(), self.coaccessible()
		AC = A.intersection(C)

		ncfg = self.spawn()
		for p, w in self.P:
			if p.head in AC and w != self.R.zero:
				invalid = False
				for elem in p.body:
					if isinstance(elem, NT) and elem not in AC:
						invalid = True
				if not invalid:
					ncfg.add(w, p.head, *p.body)

		ncfg.make_unary_fsa()
		#ncfg.freeze()
		return ncfg

	def nozero(self):
		ncfg = self.spawn()
		for p, w in self.P:
			if w != self.R.zero:
				ncfg.add(w, p.head, *p.body)

		ncfg.make_unary_fsa()
		#ncfg.freeze()
		return ncfg

	@classmethod
	def from_string(cls, string, R, comment="#"):
		cfg = CFG(R=R)
		for line in string.split("\n"):
			line = line.strip()
			if line[0] == comment:
				continue

			head_str, tmp = line.split("→")
			tail_str, weight = tmp.split("\t")
			tail_str = tail_str.strip().split(" ")

			head = NT(head_str.strip())
			tail = []
			for x in tail_str:
				x = x.strip()
				if x.islower():
					x = Sym(x)
				elif x.isupper():
					x = NT(x)
				tail.append(x)

			cfg.add(R(float(weight)), head, *tail)

		cfg.make_unary_fsa()
		return cfg

	def to_fsta(self):
		# FSTA code
		raise NotImplementedError

	def in_cnf(self):
		"""check if grammar is in cnf"""
		for p, w in self.P:
			(head, body) = p
			if head == self.S and len(body) == 1 and body[0] == ε:
				# S → ε
				continue
			elif head in self.V and len(body) == 2 and all([elem in self.V and elem != self.S for elem in body]):
				# A → B C
				continue
			elif head in self.V and len(body) == 1 and body[0] in self.Sigma and body[0] != ε:
				# A → a
				continue
			else:
				return False
		return True

	def shift_reduce(self):
		return self.bottom_up()

	def bottom_up(self):
		# PDA code
		raise NotImplementedError

	def top_down(self):
		# PDA code
		raise NotImplementedError

	def cyclic(self, reverse = True):
		"""
		Returns True if grammar is cyclic and (reverse) topological ordering if it is acyclic
		"""
		def has_cycles(X):
			nonlocal counter
			𝜷[X] = Boolean.one
			started[X] = counter
			counter += 1
			X_productions = (p for p,w in self.P if p[0]==X and w!=self.R.zero)
			for p in X_productions:
				_, body = p
				for elem in body:
					if elem in self.Sigma:
						continue
					elif 𝜷[elem] == Boolean.one: # cycle detected
						return True
					elif has_cycles(elem): # propagate cycle
						return True
			𝜷[X] = Boolean.zero
			return False

		𝜷 = Boolean.chart()
		started = {}
		counter = 0
		cyclic = has_cycles(self.S)
		if reverse:
			sort = [k for k, v in sorted(started.items(), key=lambda item: item[1])]
		else:
			sort = [k for k, v in sorted(started.items(), key=lambda item: item[1], reverse=True)]
		return cyclic, sort

	def intersect_fsa(self, fsa):
		"""
		Intersects cfg with fsa and returns the resulting parse-forest grammar
		Semiringified weighted case from Nederhof and Satta (2003)
		"""
		assert self.R == fsa.R

		pfg = self.spawn()

		def get_intersecting_rule(head, body, qs):
			NTs = []
			new_head = Triplet(qs[0], head, qs[-1])

			for i in range(len(qs)-1):
				NTs.append(Triplet(qs[i], body[i], qs[i+1]))

			if len(NTs) == 0:
				NTs.append(ε)
			return new_head, NTs

		# rules from cfg
		for p, w in self.P:
			(head, body) = p
			if len(body) == 1 and body[0] == ε:
				for q in product(fsa.Q, repeat=1):
					h, b = get_intersecting_rule(head, body, q)
					pfg.add(w, h, *b)
			else:
				for qs in product(fsa.Q, repeat=len(body)+1):
					h, b = get_intersecting_rule(head, body, qs)
					pfg.add(w, h, *b)

		# S rules
		for qi, _ in fsa.I:
			for qf, _ in fsa.F:
				b = Triplet(qi, self.S, qf)
				pfg.add(self.R.one, self.S, b)

		# terminal rules
		for i in fsa.Q:
			for a, j, w in fsa.arcs(i):
				h = Triplet(i, a, j)
				pfg.add(w, h, a)

		return pfg


	def to_latex(self):
		"""
		Prints production rules in latex syntax
		"""
		latex = []
		for p, w in self.P:
			latex.append(f"& \weightedproduction{{\\text{{{str(p.head)}}}}}" +
									 f"{{\\text{{{' '.join([str(child) for child in p.body])}}}}}" +
									 f"{{\\text{{{str(w)}}}}}")
		latex = "\\\\ \n".join(latex)
		print(latex)

	def __str__(self):
		return "\n".join(f"{p}\t{w}" for (p, w) in sorted(self.P, key=lambda x: (len(str(x[0].head)), str(x[0].head), len(str(x[0])))))
		#return "\n".join(f"{p}" for (p, w) in sorted(self.P, key=lambda x: (len(str(x[0].head)), str(x[0].head), len(str(x[0])))))

