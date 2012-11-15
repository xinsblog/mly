import regex
import nfa
import dfa
import easylex

string = raw_input("Input your regular expression:")
tstring = raw_input("Input a string for test:")
r = regex.Regex(string)
print r.toPostfix()
n = r.toNFA()
d = n.toDFA()
d.minStates()
d.show()
print d.accept(tstring)