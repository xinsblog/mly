import regex
import nfa
import dfa

regex = regex.Regex('(a|b)*abb')
n = regex.toNFA()
d = n.toDFA()
d.minStates().show()