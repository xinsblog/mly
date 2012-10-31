import regex
import nfa
import dfa

# string = '(a|b)*a(a|b)(a|b)'
# tstring = 'b'

string = raw_input("Input your regular expression:")
tstring = raw_input("Input a string for test:")
r = regex.Regex(string)
print r.toPostfix()
n = r.toNFA()
# n.show()

print '---------------------'
d = n.toDFA();
# d.show()
# # print d.accept(tstring)

print '---------------------'
d = d.minStates()
d.show()
print d.accept(tstring)