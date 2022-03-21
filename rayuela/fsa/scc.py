import numpy as np
from numpy import linalg as LA

from collections import deque

from rayuela.base.semiring import Boolean, Real
from rayuela.fsa.pathsum import Pathsum, Strategy
from rayuela.fsa.fsa import FSA
from rayuela.fsa.state import MinimizeState

class SCC:

    def __init__(self, fsa):
        self.fsa = fsa

    def scc(self):
        """
        Computes the SCCs of the FSA.
        Currently uses Kosaraju's algorithm.

        Guarantees SCCs come back in topological order.
        """
        for scc in self._kosaraju():
            yield scc

    def _kosaraju(self):
        """
        Kosaraju's algorithm [https://en.wikipedia.org/wiki/Kosaraju%27s_algorithm]
        Runs in O(E + V) time.
        Returns in the SCCs in topologically sorted order.
        """
		# Homework 3: Question 4
        raise NotImplementedError
