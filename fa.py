class FA(object):
	"""docstring for FA"""
	def __init__(self, arg):
		super(FA, self).__init__()
		self.rules = list()
		self.finalstates = list()
		self.rules.append(arg, 0, 1)
		self.finalstates.append(1)

	def addRule(self, rule):
		self.rules.append(rules)
	
	def join(self, fa):
		pass

	def union(self, fa):
		pass

	def closure(self):
		pass

	def getRules(self):
		return self.rules