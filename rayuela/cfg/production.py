from collections import namedtuple

class Production(namedtuple("Production", "head, body")):

	def __repr__(self):
		return str(self.head) + " → " +  " ".join(map(str, self.body))
