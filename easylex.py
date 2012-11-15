import json
from collections import deque

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
			if op=='B' and (result[len(result)-1]!='\\' or isEacaped==True):
				result += '( |\n)'
			if op=='D' and (result[len(result)-1]!='\\' or isEacaped==True):
				result += '(0|1|2|3|4|5|6|7|8|9)'
		return result[1:]



if __name__ == '__main__':
	lex = EasyLex()
	lex.preprocess('ABD')