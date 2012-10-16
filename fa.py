from collections import deque

class FA(object):
	namesize = 0
	EPSILON = 'EPSILON'
	"""docstring for FA"""
	def __init__(self, arg):
		super(FA, self).__init__()
		self.rules = dict()
		self.startState = -1
		self.finalState = -1
		self.rules[self.__class__.namesize] = [[arg, self.__class__.namesize+1]]
		self.rules[self.__class__.namesize+1] = list()
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
		self.rules[newf] = list()
		self.startState = news
		self.finalState = newf
		self.__class__.namesize += 2
		
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
		self.rules[newf] = list()
		self.startState = news
		self.finalState = newf
		self.__class__.namesize += 2

	def show(self):
		for key in self.rules.keys():
			print key, ':', self.rules[key]
		print 'start state:', self.startState
		print 'final state:', self.finalState
		print 'namesize:', self.__class__.namesize

	def toDFA(self, exp):
		operators = ('*', '+', '|')
		alphabet = set(exp) - set(operators)
		alphabet = list(alphabet)
		count = 65
		key = chr(count)
		# mapping from new keys to the aggregated states
		states = dict() 	
		states[key] = self.findEpsilon([self.startState])
		# record relations between keys
		paths = dict()
		# store the keys to be processed
		queue = deque(list())
		queue.append(key)
		while len(queue):
			newkey = queue.popleft()
			for c in alphabet:
				newstate = self.findCondition(states[newkey], c)
				newstate = self.findEpsilon(newstate)
				key = self.getKey(states, newstate)
				if key==0:
					count += 1
					key = chr(count)
					states[key] = newstate
					queue.append(key)
				if paths.has_key(newkey)==False:
					paths[newkey] = dict()
				paths[newkey][c] = key
		sStates = list()
		fStates = list()
		for key in states.keys():
			if self.startState in states[key]:
				sStates.append(key)
			if self.finalState in states[key]:
				fStates.append(key)
		# print 'state:', states
		# print 'paths:', paths
		# print 'starting states:', sStates
		# print 'ending states:', fStates
		dfa = {'state':states, 'paths':paths, 'sStates':sStates, 'fStates':fStates, 'alphabet':alphabet}
		return dfa

	def getKey(self, states, state):
		for key in states.keys():
			if state == states[key]:
				return key
		return 0


	def findEpsilon(self, outset):
		result = set(outset)
		while True:
			flag = True
			for i in outset:
				for rule in self.rules[i]:
					if (rule[0]==self.__class__.EPSILON) & (rule[1] not in result):
						result.add(rule[1])
						flag = False
			outset = list(result)
			if flag:
				return result

	def findCondition(self, outset, c):
		result = set()
		for i in outset:
			for rule in self.rules[i]:
				if (rule[0]==c) & (rule[1] not in result):
					result.add(rule[1])
		return result

	def accept(self, dfa, string):
		exp = list(string)
		reached = list()
		paths = dfa['paths']
		for s in dfa['sStates']:
			flag = True
			for op in exp:
				if paths[s].has_key(op):
					s = paths[s][op]
				else:
				 	flag = False
			if flag & (s in dfa['fStates']):
				reached.append(s)
		if len(reached):
			return True
		else:
			return False

	def minStates(self, dfa):
		paths = dfa['paths']
		fStates = set(dfa['fStates'])	
		states = set(paths.keys())
		nfStates = states - fStates
		partition = list()
		partition.append(nfStates)
		partition.append(fStates)
		flag = True
		while flag:
			flag = False
			newpartition = list()
			for i in range(len(partition)):
				part = dict()
				for s in partition[i]:
					part[s] = self.getPart(s, dfa, partition)
				mapping = list()
				newpart = list()
				for s in partition[i]:
					if part[s] not in mapping:
						mapping.append(part[s])
						newpart.append(set())
				for s in partition[i]:
					for j in range(len(mapping)):
						if part[s]==mapping[j]:
							newpart[j].add(s)
				if len(newpart)>1:
					flag = True
				newpartition.extend(newpart)
			partition = newpartition
		newstates = [list(part)[0] for part in partition]
		category = {list(part)[0]:list(part)[1:] for part in partition}
		print category
		newpaths = dict()
		alphabet = dfa['alphabet']
		for state in newstates:
			newpaths[state] = dict()
			for a in alphabet:
				b = paths[state][a]
				if b in newstates:
					newpaths[state][a] = b
				else:
					for key in category.keys():
						if b in category[key]:
							newpaths[state][a] = key
							break
		newfStates = set()
		for state in newstates:
			if state in fStates:
				newfStates.add(state)
		newsStates = set(newstates) - newfStates
		print newsStates
		print newfStates

	def getPart(self, state, dfa, partition):
		paths = dfa['paths']
		alphabet = dfa['alphabet']
		result = list()
		for a in alphabet:
			dist = paths[state][a]
			for i in range(len(partition)):
				if dist in partition[i]:
					result.append(i)
					break
		return result

def toNFA(exp):
	operators = ('*', '+', '|')
	stack = list()
	for op in exp:
		if op not in operators:
			stack.append(FA(op))
		elif op == '*':
			fa = stack.pop()
			fa.closure()
			stack.append(fa)	
		elif op == '+':
			fa1 = stack.pop()			
			fa2 = stack.pop()
			fa2.join(fa1)
			stack.append(fa2)
		elif op == '|':
			fa1 = stack.pop()
			fa2 = stack.pop()
			fa2.union(fa1)
			stack.append(fa2)
	return stack[0]
	
exp = 'ab|*a+b+b+'
fa = toNFA(exp)
dfa = fa.toDFA(exp)
# fa.accept(dfa, 'ac')
print dfa['paths']
fa.minStates(dfa)