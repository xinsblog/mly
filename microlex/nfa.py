from collections import deque
import dfa

class NFA(object):
    namesize = 0
    EPSILON = 'EPSILON'
    """docstring for FA"""
    def __init__(self, op, exp):
        super(NFA, self).__init__()
        self.exp = exp
        self.rules = dict()
        self.startState = -1
        self.finalState = -1
        self.rules[self.__class__.namesize] = [[op, self.__class__.namesize+1]]
        self.rules[self.__class__.namesize+1] = list()
        self.startState = self.__class__.namesize
        self.finalState = self.__class__.namesize+1
        self.__class__.namesize += 2

    def closure(self):
        s = self.startState
        f = self.finalState
        news = self.__class__.namesize
        newf = self.__class__.namesize+1
        if self.rules.has_key(news)==False:
            self.rules[news] = list()
        if self.rules.has_key(f)==False:
            self.rules[f] = list()
        self.rules[news].append([self.__class__.EPSILON, s])
        self.rules[news].append([self.__class__.EPSILON, newf])
        self.rules[f].append([self.__class__.EPSILON, newf])
        self.rules[f].append([self.__class__.EPSILON, s])
        self.rules[newf] = list()
        self.startState = news
        self.finalState = newf
        self.__class__.namesize += 2

    def join(self, fa):
        self.rules.update(fa.rules)
        linkf = self.finalState
        links = fa.startState
        if self.rules.has_key(linkf)==False:
            self.rules[linkf] = list()
        self.rules[linkf].extend(self.rules[links])
        self.rules.pop(links)
        self.finalState = fa.finalState

    def union(self, fa):
        self.rules.update(fa.rules)
        s1 = self.startState
        f1 = self.finalState
        s2 = fa.startState
        f2 = fa.finalState
        news = self.__class__.namesize
        newf = self.__class__.namesize+1
        self.rules[news] = list()
        if self.rules.has_key(f1)==False:
            self.rules[f1] = list()
        if self.rules.has_key(f2)==False:
            self.rules[f2] = list()
        self.rules[news].append([self.__class__.EPSILON, s1])
        self.rules[news].append([self.__class__.EPSILON, s2])
        self.rules[f1].append([self.__class__.EPSILON, newf])
        self.rules[f2].append([self.__class__.EPSILON, newf])
        self.rules[newf] = list()
        self.startState = news
        self.finalState = newf
        self.__class__.namesize += 2

    # list states store the mappint relation from the NFA to DFA
    def toDFA(self):
        exp = self.exp
        operators = ('*', '+', '|')
        alphabet = set(exp) - set(operators)
        alphabet = list(alphabet)
        count = 0
        key = str(count)
        # mapping from new keys to the aggregated states
        states = dict()
        states[key] = self.findEpsilon([self.startState])
        # record relations between keys
        paths = dict()
        # store the keys to be processed
        queue = deque(list())
        queue.append(key)
        while len(queue):
            newkey = queue.popleft()
            for c in alphabet:
                newstate = self.findCondition(states[newkey], c)
                newstate = self.findEpsilon(newstate)
                key = self.getKey(states, newstate)
                if key==0:
                    count += 1
                    key = str(count)
                    states[key] = newstate
                    queue.append(key)
                if paths.has_key(newkey)==False:
                    paths[newkey] = dict()
                paths[newkey][c] = key
        sStates = list()
        fStates = list()
        for key in states.keys():
            if self.startState in states[key]:
                sStates.append(key)
            if self.finalState in states[key]:
                fStates.append(key)
        # print states
        states = states.keys()
        d = dfa.DFA()
        d.setStates(states, paths, sStates, fStates, alphabet)
        return d
        # return dfa.DFA(states, paths, sStates, fStates, alphabet)

    def getKey(self, states, state):
        for key in states.keys():
            if state == states[key]:
                return key
        return 0

    def findEpsilon(self, outset):
        result = set(outset)
        while True:
            flag = True
            for i in outset:
                for rule in self.rules[i]:
                    if (rule[0]==self.__class__.EPSILON) & (rule[1] not in result):
                        result.add(rule[1])
                        flag = False
            outset = list(result)
            if flag:
                return result

    def findCondition(self, outset, c):
        result = set()
        for i in outset:
            for rule in self.rules[i]:
                if (rule[0]==c) & (rule[1] not in result):
                    result.add(rule[1])
        return result

    def show(self):
        print 'rules:'
        keys = self.rules.keys()
        for key in keys:
            print str(key), ':', self.rules[key]
        print 'startState:', self.startState
        print 'finalState:', self.finalState
        print 'namesize:', self.__class__.namesize
