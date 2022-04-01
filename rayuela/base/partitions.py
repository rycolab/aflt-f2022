import random
import numpy as np
from collections import defaultdict as dd
from itertools import product

class PartitionRefinement:

	def __init__(self, f, Q):
	
		self.f = f
		self.Q = Q

		# compute the pre-image of f
		self.finv = dd(lambda : set([]))
		for n in Q: self.finv[self.f[n]].add(n)

	def stable(self, P):

		# definition of stable
		D = {}
		for n, B in enumerate(P):
			for q in B:
				D[q] = n

		for B in P:
			for p in B:
				for q in B:
					if D[self.f[p]] != D[self.f[q]]:
						return False
		return True

	def split(self, S, P):
		""" runs in O(|P|) time if Python is clever """
		return frozenset(P&S), frozenset(P-S)

	def naive(self, P):

		stack = list(P)

		while stack: # empties in O(|Q|) steps			
			S = stack.pop()
			R = set([]) # new refinement
			
			# compute subset of the pre-image in O(|Q|) time
			Sinv = set([]).union(*[self.finv[x] for x in S])

			for B in P: # entire loop runs in O(|Q|) time
				X, Y = self.split(Sinv, B) # runs in O(|B|) time

				if len(X) > 0 and len(Y) > 0:
					# X, Y are now part of the refinement
					R.add(X)
					R.add(Y)

					# X, Y become future splitters
					stack.append(X)
					stack.append(Y)
				else:
					# B remains part of the refinement
					R.add(B)
			P = R
			
		assert self.stable(P)
		return frozenset(P)

	def hopcroft(self, P):

		stack = list(P)
		while stack: # empties in O(log|Q|) steps			
			S = stack.pop()
			R = set([]) # new refinement
			
			# compute subset of the pre-image in O(|Q|) time
			Sinv = set([]).union(*[self.finv[x] for x in S])

			for B in P: # entire loop runs in O(|Q|) time
				X, Y = self.split(Sinv, B) # runs in O(|B|) time

				if len(X) > 0 and len(Y) > 0:
					# X, Y are now part of the refinement
					R.add(X)
					R.add(Y)

					if B in stack:	
						stack.remove(B)
						stack.append(X)
						stack.append(Y)
					else:
						if len(X) < len(Y):
							stack.append(X)
						else:
							stack.append(Y)

				else:
					# B remains part of the refinement
					R.add(B)
			P = R
			
		assert self.stable(P)
		return frozenset(P)

	def hopcroft_fast(self, P):

		raise NotImplementedError

	def moore(self, P):

		raise NotImplementedError