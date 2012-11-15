import json
data = [ { 'a':'A', 'b':(2, 4), 'c':3.0 } ]
f = open('test.txt', 'w')
json.dump(data, f)
f.flush()
