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

		# handle unaries outside of main loops

		W = Pathsum(self.cfg.unary_fsa).lehmann(zero=False)
		chain = lambda X, Y: W[State(X), State(Y)] if (State(X), State(Y)) in W else self.R.zero

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

				# include unary chains (not part of standard CKY)
				U = []
				for X in self.cfg.V:
					for Y in self.cfg.V:
						U.append(((Y, i, k), β[(X, i, k)] * chain(X, Y)))
				for item, w in U:
					β[item] += w

		return β

	def faster_cky(self, input, unary=True):
		return self._faster_cky(input, unary=unary)[(self.cfg.S, 0, len(input))]

	def _faster_cky(self, input, unary=False):
		# Assignment 8
		raise NotImplementedError