import regex
import nfa
import dfa
import json

string = raw_input("Input your regular expression:")
print '---------------------'
r = regex.Regex(string)
n = r.toNFA()
n.show()

print '---------------------'
d = n.toDFA();
d.show()

print '---------------------'
d = d.minStates()
d.show()