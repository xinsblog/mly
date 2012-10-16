class FA(object):
	namesize = 0
	EPSILON = 'EPSILON'
	"""docstring for FA"""
	def __init__(self, arg):
		super(FA, self).__init__()
		self.rules = dict()
		self.startState = -1
		self.finalState = -1
		self.rules[self.__class__.namesize] = [arg, self.__class__.namesize+1]
		self.startState = self.__class__.namesize
		self.finalState = self.__class__.namesize+1
		self.__class__.namesize += 2

	def closure(self):
		s = self.startState
		f = self.finalState
		news = self.__class__.namesize
		newf = self.__class__.namesize+1
		if self.rules.has_key(news)==False:
			self.rules[news] = list()
		if self.rules.has_key(f)==False:
			self.rules[f] = list()
		self.rules[news].append([self.__class__.EPSILON, s])
		self.rules[news].append([self.__class__.EPSILON, newf])
		self.rules[f].append([self.__class__.EPSILON, newf])
		self.rules[f].append([self.__class__.EPSILON, s])
		self.startState = news
		self.finalState = newf
		self.namesize += 2
		
	def join(self, fa):
		self.rules.update(fa.rules)
		linkf = self.finalState
		links = fa.startState
		if self.rules.has_key(linkf)==False:
			self.rules[linkf] = list()
		self.rules[linkf].extend(self.rules[links])
		self.rules.pop(links)
		self.finalState = fa.finalState

	def union(self, fa):
		self.rules.update(fa.rules)
		s1 = self.startState
		f1 = self.finalState
		s2 = fa.startState
		f2 = fa.finalState
		news = self.__class__.namesize
		newf = self.__class__.namesize+1
		self.rules[news] = list()
		if self.rules.has_key(f1)==False:
			self.rules[f1] = list()
		if self.rules.has_key(f2)==False:
			self.rules[f2] = list()
		self.rules[news].append([self.__class__.EPSILON, s1])
		self.rules[news].append([self.__class__.EPSILON, s2])
		self.rules[f1].append([self.__class__.EPSILON, newf])
		self.rules[f2].append([self.__class__.EPSILON, newf])
		self.startState = news
		self.finalState = newf
		self.namesize += 2

	def toDFA(self):
		pass

	def accept(self):
		pass		

	def show(self):
		for key in self.rules.keys():
			print key, ':', self.rules[key]
		print 'start state:', self.startState
		print 'final state:', self.finalState


def toNFA(exp):
	operators = ('*', '+', '|')
	stack = list()
	for op in exp:
		print op
		if op not in operators:
			stack.append(FA(op))
			stack[0].show()
		elif op == '*':
			fa = stack.pop()
			fa.closure()
			stack.append(fa)	
			stack[0].show()
		elif op == '+':
			fa1 = stack.pop()			
			fa2 = stack.pop()
			fa2.join(fa1)
			stack.append(fa2)
			stack[0].show()
		elif op == '|':
			fa1 = stack.pop()
			fa2 = stack.pop()
			fa2.union(fa1)
			stack.append(fa2)
			stack[0].show()
	return stack[0]
	
fa = toNFA('a*b|')
# fa.show()