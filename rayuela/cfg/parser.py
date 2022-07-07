from collections import defaultdict as dd
from itertools import product
import numpy as np

from rayuela.base.datastructures import PriorityQueue
from rayuela.base.semiring import Real, Tropical
from rayuela.base.misc import symify
from rayuela.base.symbol import Sym

from rayuela.fsa.state import State
from rayuela.fsa.pathsum import Pathsum
from rayuela.fsa.pathsum import Strategy

from rayuela.cfg.cfg import CFG
from rayuela.cfg.production import Production
from rayuela.cfg.nonterminal import S, NT, Slash, Other


class Parser:

	def __init__(self, cfg):
		self.cfg = cfg
		self.R = self.cfg.R

	def sum(self, input, strategy="cky"):
		if strategy == "cky":
			return self.cky(input)
		elif strategy == "faster-cky":
			raise self.faster_cky(input)
		else:
			raise NotImplementedError

	def cky(self, input, unary=True):
		return self._cky(input, unary=unary)[(self.cfg.S, 0, len(input))]

	def _cky(self, input, unary=False):
		""" semiring version of CKY  """
		N = len(input)

		# initialization
		β = self.R.chart()

		# pre-terminals
		for (head, body), w in self.cfg.terminal:
			for i in range(N):
				if body[0] == input[i]:
					β[head, i, i+1] += w

		# three for loops
		for span in range(1, N+2):
			for i in range(N-span+1):
				k = i + span
				for j in range(i+1, k):
					for p, w in self.cfg.binary:
						X, Y, Z = p.head, p.body[0], p.body[1]
						β[X, i, k] += β[Y, i, j] * β[Z, j, k] * w

		return β

	def faster_cky(self, input, unary=True):
		return self._faster_cky(input, unary=unary)[(self.cfg.S, 0, len(input))]

	def _faster_cky(self, input, unary=False):
		# Assignment 8
		raise NotImplementedError


class EarleyItem:

	def __init__(self, i, k, head, body=(), dot=0, star=False, dotopt=False):
		self.i, self.k = i, k
		self.head, self.body = head, body
		assert self.i <= self.k, "inadmissible span"
		self.dot = dot
		self.star = star

	def __str__(self):
		body = []
		for n, X in enumerate(self.body):
			if n == self.dot: body.append("•")
			body.append(str(X))
		if self.dot == len(self.body):
			body.append("•")
		body = " ".join(body)

		return f"[{self.i}, {self.k}, {self.head} → {body}]"

	def __repr__(self):
		return str(self)

	def __eq__(self, other):
		return isinstance(other, EarleyItem) and \
			   self.i == other.i and self.k == other.k and \
			   self.head == other.head and self.body == other.body and \
			   self.dot == other.dot

	def __hash__(self):
		return hash((self.i, self.k, self.dot, self.head, self.body))


class EarleyParser(Parser):

	def __init__(self, cfg):
		super().__init__(cfg)

	def _earley(self, input):
		# Assignment 8, Question 4
		raise NotImplementedError

	def earley(self, input, strategy="earley"):
		β = None
		if strategy == "earley":
			β = self._earley(input)
		else:
			raise NotImplementedError

		total = self.cfg.R.zero
		for item, w in β.items():
			if item.end and item.head == S and item.i == 0 and item.k == len(input):
				total += β[item]

		return total