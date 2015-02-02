
import json

import parsing_state
import parsing_chart


def _reduction(c, i):
    while True:
        length = len(c.get_row(i))
        rdt_states = []
        for j in range(len(c.get_row(i))):
            if c.get([i,j]).cd == [] :
                rdt_states += c.get_row(i)[j].reduction(c, [i, j])
        c.add(rdt_states, i)
        if length == len(c.get_row(i)):
            break


def _closure(c, grammar, i):
    while True:
        length = len(c.get_row(i))
        cls_states = []
        for j in range(len(c.get_row(i))):
            cls_states += c.get([i,j]).closure(grammar, cf=[i,j])
        c.add(cls_states, i)
        if length == len(c.get_row(i)):
            break


def _fill_chart(grammar, expr, initial, epsilon):
    chart = parsing_chart.ParsingChart()
    # init the chart
    for g in grammar:
        if g[0] == initial:
            s = parsing_state.ParsingState(g[0], [], g[1], [0,0], [-1,-1], [-1,-1])
            chart.add([s], 0)

    # compute the initial closure
    _closure(chart, grammar, 0)
    # start to use the chart to track each step
    for i in range(1, len(expr)+1):
        token = expr[i-1]
        chart.extend()
        # shift all the possible state in chart[i-1]
        # if no states could be shfited, then the input text is illegal
        ss = [ chart.get([i-1,j]).shift(sf=[i-1, j])
                for j in range(len(chart.get_row(i-1)))
                    if  chart.get([i-1,j]).cd != [] and chart.get([i-1, j]).cd[0] == token ]
        if not ss:
            return [False, chart]
        chart.add(ss, i)
        while True:
            length = len(chart.get_row(i))
            _reduction(chart, i)
            _closure(chart, grammar, i)
            #handle the epsilon case
            ss = [chart.get([i,j]).shift(sf=[i, j])
                for j in range(len(chart.get_row(i)))
                    if  chart.get([i,j]).cd != [] and chart.get([i,j]).cd[0] == epsilon]
            chart.add(ss, i)
            if length == len(chart.get_row(i)):
                break
    return [True, chart]


def _expand(state, chart, terminals):
    stack = list()
    ss = state.ab
    ss.reverse()
    for s in ss:
        if s in terminals:
            stack.append([s])
        else:
            stack.append([s, _expand(chart.get(state.rf), chart, terminals)])
        state = chart.get(state.sf)
    stack.reverse()
    return stack


def parse(grammar, expr, initial, epsilon, terminals):
    ''' Generate a parsing for the expr according to the context-free grammar.

    :param
        grammar : list
            definition of the context-free grammar
        expr :  list
            the expression to parse
        initial : string
            the start symbol
        epsilon : string
            the empty symbol

    :return
        [True, parsing_tree] if expr is successfully parsed
        [False, []] Otherwise

    '''

    [ret, ch] = _fill_chart(grammar, expr, initial, epsilon)
    if ret is False:
        return [False, []]
    cands = list()
    for ps in ch.get_row(ch.len()-1):
        if ps.x == initial and ps.cd == [] and ps.cf[0] == 0:
            cands.append(ps)
    if len(cands) != 1:
        return [False, []]
    tree = [cands[0].x, _expand(cands[0], ch, terminals)]
    return [True, tree]






