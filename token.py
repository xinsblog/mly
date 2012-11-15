class Token(object):
	"""docstring for Token"""
	def __init__(self, t, value, lineno):
		self.type = t
		self.value = value		
		self.lineno = lineno

	def show(self):
		print 'type:', self.type, 'value:', self.value, 'lineno:', self.lineno