from collections import deque

def process(string):
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
			show(op, charStack, operatorStack)
		elif op == '*':
			a = charStack.pop()
			a = a + op
			charStack.append(a)
			show(op, charStack, operatorStack)
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
			show(op, charStack, operatorStack)
		elif op == '#':
			o = operatorStack.pop()
			while o!='#':
				a = charStack.pop()
				b = charStack.pop()
				newChar = b+a+o
				charStack.append(newChar)
				o = operatorStack.pop()
			show(op, charStack, operatorStack)
		else:
			o = operatorStack.pop()
			if prior[op]<=prior[o]:
				a = charStack.pop()
				b = charStack.pop()
				newChar = b+a+o
				charStack.append(newChar)
				operatorStack.append(op)
				show(op, charStack, operatorStack)
			else:
				operatorStack.append(o)
				operatorStack.append(op)
				show(op, charStack, operatorStack)
	print charStack
	return charStack

# preprocess the regular expression
# add the "join" operator in different segment
def  preprocess(string):
	metachars = ('(', ')', '+', '|', '*')
	exp = list(string)
	for i in range(len(exp)-1, 0, -1):
		if (exp[i] not in metachars) & (exp[i-1] not in metachars):
			exp.insert(i, '+')
	return exp

# postprocess the result of charStack
# combine each segment
def postprocess(charStack):
	postfix = charStack[0]
	for i in range(1, len(postfix)):
		postfix += charStack[i] + '+'
	return postfix

# translate the expression from middle-fix to postfix
def toPostfix(string):
	string = preprocess(string)
	charStack = process(string)
	postfix = postprocess(charStack)
	return postfix

# show the two stacks during the translation
def  show(op, charStack, operatorStack):
	print op, ':', charStack, operatorStack

print toPostfix('(ab)c*(c|d)*')

