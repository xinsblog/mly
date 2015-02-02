
# define a chart, a chart is a list of states at each step


class ParsingChart:

    def __init__(self):
        self.chart = [[]]

    def len(self):
        return len(self.chart)

    # extend the length of chart by 1
    def extend(self):
        self.chart.append([])

    # add a list of states at position i
    def add(self, states, i):
        for state in states:
            if self.has(state, i):
                pass
            else :
                self.chart[i] += [state]

    # get the list of states at position i
    def get_row(self, i):
        return self.chart[i]

    # get a state by the index (i, j)
    def get(self, idx):
        [i, j] = idx
        return self.chart[i][j]

    def has(self, state, i):
        for s in self.chart[i]:
            if s.equals(state):
                return True
        return False

    def has_terminal(self, end_state):
        for state in self.get_row(len(self.chart)-1):
            if state.x==end_state.x and state.ab==end_state.ab and state.cd==end_state.cd:
                return True
        return False

    def show(self):
        for i in range(len(self.chart)):
            print 'i =', i
            for state in self.chart[i]:
                state.show()
        print ''