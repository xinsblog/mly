import json
from collections import deque

import regex 
import nfa
import dfa
import token

class EasyLex(object):
	def __init__(self):
		super(EasyLex, self).__init__()

	def preprocess(self, string):
		exp = list(string)
		exp = deque(exp)
		result = '#'
		while len(exp):
			op = exp.popleft()
			if op=='A' and (result[len(result)-1]!='\\' or isEacaped==True):
				result += '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)'
			elif op=='B' and (result[len(result)-1]!='\\' or isEacaped==True):
				result += '( )'
				continue
			elif op=='D' and (result[len(result)-1]!='\\' or isEacaped==True):
				result += '(0|1|2|3|4|5|6|7|8|9)'
			else:
				result += op
		return result[1:]

	def generateRules(self):
		fr = open(name='test.pl', mode='r')
		rules = dict()
		rules['names'] = list()
		while True:
			line = fr.readline()
			if not line:
				break
			else:
				data = line.split(':')
				rules['names'].append(data[0])
				exp = self.preprocess(data[1][0:len(data[1])-1])
				r = regex.Regex(exp)
				n = r.toNFA()
				d = n.toDFA()
				d.minStates()
				rules[data[0]] = d.encode()
		print rules
		fw = open('test.dfa', 'w')
		json.dump(rules, fw)
		fw.flush()

	def importRules(self):
		fr = open('test.dfa', 'r')		
		data = json.load(fr)
		rules = dict()
		# order is a list which define the order of the rules
		order = data['names']
		rules['order'] = order
		for name in order:
			d = dfa.DFA()
			d.decode(data[name])
			rules[name] = d
		return rules
		
								
	def analyze(self, rules):
		fsrc = open('test.c', 'r')
		lineno = 0
		order = rules['order']
		commentRule = rules['comment']
		ignoreRule = rules['ignore']
		tokens = list()
		while True:
			# read a line of string from the source code file
			lineno += 1
			line = fsrc.readline()
			if not line:
				break
			line = line[0:len(line)-1]
			# get accross the comment part
			isCommented = False
			for i in xrange(0, len(line)):
				if commentRule.accept(line[i:len(line)]):
					isCommented = True
					break;
			if i==0:
				continue
			elif isCommented:
				line = line[0:i]
			else:
				line = line[0:i+1]
			# divide a line into small sections based on the ignored character
			sections = list()
			headindex = 0
			endindex = 0
			for i in xrange(0,len(line)):
				if ignoreRule.accept(line[i]) and headindex==endindex:
					headindex += 1
					endindex += 1
				elif ignoreRule.accept(line[i]):
					sections.append(line[headindex:endindex])
					endindex += 1
					headindex = endindex
				else:
					endindex +=1 
			if headindex!=endindex:
				sections.append(line[headindex:endindex])
			# get tokens from each section
			for section in sections:
				line = section
				headindex = 0
				endindex = len(line)
				while headindex<len(line):
					endindex = len(line)
					while endindex>0:
						string = line[headindex:endindex]
						for name in order :
							if rules[name].accept(string):
								t = token.Token(name, string, lineno)	
								tokens.append(t)
								headindex = endindex
								break
						endindex -= 1
		return tokens


if __name__ == '__main__':
	lex = EasyLex()
	while True:
		choice = raw_input('''
			1.generate new rules from test.pl
			2.analyze source code from test.c
			3.quit
			Enter your choice
			''');
		if choice=='1':
			lex.generateRules()
		elif choice=='2':
			tokens = lex.analyze(lex.importRules())
			for t in tokens:
				t.show()
		elif choice=='3':
			break;
