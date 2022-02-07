from frozendict import frozendict

class State:

	def __init__(self, idx, label=None):
		self._idx = idx
		self._label = label

	@property
	def idx(self):
		return self._idx
	
	@property
	def label(self):
		return self._label

	def set_label(self, label):
		self._label = label

	def copy(self):
		return State(self.idx)

	def __repr__(self):
		if self.label is not None:
			return f'{self.label}'
		return f'{self.idx}'

	def __str__(self):
		if self.label is not None:
			return f'{self.label}'
		return str(self.idx)

	def __hash__(self):
		return hash(self.idx)

	def __eq__(self, other):
		return isinstance(other, State) and self.idx == other.idx


class PairState(State):

	def __init__(self, p, q):
		super().__init__((p, q))

	@property
	def state1(self):
		return self.idx[0]

	@property
	def state2(self):
		return self.idx[1]

	def __repr__(self):
		return f"( {str(self.state1)}, {str(self.state2)} )"

	def __str__(self):
		return self.__repr__()
