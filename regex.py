from collections import deque
import nfa

class Regex(object):
	"""docstring for Regex"""
	def __init__(self, exp):
		super(Regex, self).__init__()
		self.exp = exp
		

	def process(self, string):
		exp = list(string)
		operators = ('|', '*', '(', ')', '+', '#')
		prior = {'(':0, '|':1, '+':2, '*':3, '#':-1}
		charStack = list()
		operatorStack = list('#')
		exp = deque(exp)
		exp.append('#')
		while len(exp):
			op = exp.popleft()
			if op not in operators:
				charStack.append(op)
			elif op == '*':
				a = charStack.pop()
				a = a + op
				charStack.append(a)
			elif op == '(':
				operatorStack.append(op)
			elif op == ')':
				o = operatorStack.pop()
				while o!='(':
					a = charStack.pop()
					b = charStack.pop()
					newChar = b+a+o
					charStack.append(newChar)
					o = operatorStack.pop()
			elif op == '#':
				o = operatorStack.pop()
				while o!='#':
					a = charStack.pop()
					b = charStack.pop()
					newChar = b+a+o
					charStack.append(newChar)
					o = operatorStack.pop()
			else:
				o = operatorStack.pop()
				if prior[op]<=prior[o]:
					a = charStack.pop()
					b = charStack.pop()
					newChar = b+a+o
					charStack.append(newChar)
					operatorStack.append(op)
				else:
					operatorStack.append(o)
					operatorStack.append(op)
		return charStack

	# preprocess the regular expression
	# add the "join" operator in different segment
	def  preprocess(self, string):
		metachars = ('(', ')', '+', '|', '*')
		exp = list(string)
		for i in range(len(exp)-1, 0, -1):
			if (exp[i] not in metachars) & (exp[i-1] not in metachars):
				exp.insert(i, '+')
		return exp

	# postprocess the result of charStack
	# combine each segment
	def postprocess(self, charStack):
		postfix = charStack[0]
		if len(charStack)==1:
			return postfix
		for i in range(1, len(charStack)):
			if len(charStack[i])>1 and charStack[i][1]=='*':
				postfix += charStack[i][0:2] + '+' + charStack[i][2:]
			else:
				postfix += charStack[i][0] + '+' + charStack[i][1:]
		return postfix

	# translate the expression from middle-fix to postfix
	def toPostfix(self):
		string = self.exp
		string = self.preprocess(string)
		charStack = self.process(string)
		postfix = self.postprocess(charStack)
		return postfix

	# convert a regular expression to a NFA 
	def toNFA(self):
		exp = self.toPostfix()
		operators = ('*', '+', '|')
		stack = list()
		for op in exp:
			if op not in operators:
				stack.append(nfa.NFA(op, self.toPostfix()))
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
		

