
# define a state: x--->ab.cd closure form cf, shift from sf, reduce from rf


class ParsingState:
    def __init__(self, x, ab, cd, cf, sf, rf):
        self.x = x
        self.ab = ab
        self.cd = cd
        self.cf = cf
        self.sf = sf
        self.rf = rf

    def equals(self, state):
        return self.x == state.x and self.ab == state.ab and self.cd == state.cd \
               and self.cf == state.cf and self.sf == state.sf and self.rf == state.rf

    # return the closure of the state as a list
    def closure(self, grammar, cf):
        return [ParsingState(rule[0], [], list(rule[1]), cf, [-1,-1], [-1,-1])
                for rule in grammar
                    if self.cd != [] and rule[0] == self.cd[0] ]

    # return the state after right-shift as a single object
    def shift(self, sf):
        return ParsingState(self.x, self.ab+[self.cd[0]], self.cd[1:], self.cf, sf, self.rf)

    # return a list of all the reduced states
    def reduction(self, chart, rf):
        state = chart.get(self.cf)
        return [ ParsingState(state.x, state.ab+[state.cd[0]], state.cd[1:], cf=state.cf, sf=self.cf, rf=rf) ]

    def show(self):
        print self.x, '--->', self.ab, '.', self.cd
        print '\t\tclousure from ', self.cf, ', shift from ', self.sf, ' reduction from ', self.rf

