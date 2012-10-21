import regex
import nfa
import dfa
import json

string = raw_input("Input your regular expression:")
print '---------------------'
r = regex.Regex(string)
n = r.toNFA()
json_n = json.dumps({
	'startNode' : n.startState,
	'endNode' : n.finalState,
	'paths' : n.rules
});
print json_n;
print '---------------------'
d = n.toDFA();
json_d = json.dumps({
	'startNode' : list(d.sStates),
	'endNode' : list(d.fStates),
	'paths' : d.paths
});
print json_d
print '---------------------'
d = d.minStates()
json_d = json.dumps({
	'startNode' : list(d.sStates),
	'endNode' : list(d.fStates),
	'paths' : d.paths
});
print json_d