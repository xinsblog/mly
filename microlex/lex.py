import json
from collections import deque

import reg_expr
import dfa
import token


def _preprocess(string):
    exp = list(string)
    exp = deque(exp)
    result = '#'
    while len(exp):
        op = exp.popleft()
        if op == 'A' and (result[len(result)-1]!='\\'):
            result += '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)'
        elif op == 'B' and (result[len(result)-1]!='\\'):
            result += '( )'
            continue
        elif op == 'D' and (result[len(result)-1]!='\\'):
            result += '(0|1|2|3|4|5|6|7|8|9)'
        else:
            result += op
    return result[1:]


def gen_rules(infile, outfile):
    ''' Generate rules from input file, then write rules to the output file.

    :parameter
        infile : string
            path of input file('.l'), definitions of tokens in regular expressions.
        outfile : string
            path of output file, write a group of DFAs in it.
    :return
        set of the DFAs generated.
    '''

    fr = open(name=infile, mode='r')
    rules = dict()
    rules['names'] = list()
    while True:
        line = fr.readline()
        if not line:
            break
        else:
            data = line.split(':')
            rules['names'].append(data[0])
            exp = _preprocess(data[1][0:len(data[1])-1])
            r = reg_expr.RegExpr(exp)
            n = r.toNFA()
            d = n.toDFA()
            d.minStates()
            rules[data[0]] = d.encode()
    fw = open(outfile, 'w')
    json.dump(rules, fw)
    fw.flush()
    return rules


def import_rules(path):
    ''' import DFAs from rule file.

    :parameter
        path : string
            path of the rule file,
    :return
        set of the DFAs imported.
    '''

    fr = open(path, 'r')
    data = json.load(fr)
    rules = dict()

    # order is a list which define the order of the rules
    order = data['names']
    rules['order'] = order
    for name in order:
        d = dfa.DFA()
        d.decode(data[name])
        rules[name] = d
    return rules


def analyze(rules, path):
    ''' recognize the token from the source code
    :param
        rules : list
            list of DFAs
        path : string
            path of the source code
    :return
        Tokens detected.
    '''

    fsrc = open(path, 'r')
    lineno = 0
    order = rules['order']
    comment_rule = rules['comment']
    ignore_rule = rules['ignore']
    tokens = list()
    while True:
        # read a line of string from the source code file
        lineno += 1
        line = fsrc.readline()
        if not line:
            break
        line = line[0:len(line)-1]

        # get accross the comment part
        commented = False
        for i in xrange(0, len(line)):
            if comment_rule.accept(line[i:len(line)]):
                commented = True
                break
        if i == 0:
            continue
        elif commented:
            line = line[0:i]
        else:
            line = line[0:i+1]

        # divide a line into small sections based on the ignored character
        sections = list()
        headidx = 0
        endidx = 0
        for i in xrange(0,len(line)):
            if ignore_rule.accept(line[i]) and headidx==endidx:
                headidx += 1
                endidx += 1
            elif ignore_rule.accept(line[i]):
                sections.append(line[headidx:endidx])
                endidx += 1
                headidx = endidx
            else:
                endidx +=1
        if headidx!=endidx:
            sections.append(line[headidx:endidx])

        # get tokens from each section
        for section in sections:
            line = section
            headidx = 0
            endidx = len(line)
            while headidx<len(line):
                endidx = len(line)
                while endidx>0:
                    string = line[headidx:endidx]
                    for name in order :
                        if rules[name].accept(string):
                            t = token.Token(name, string, lineno)
                            tokens.append(t)
                            headidx = endidx
                            break
                    endidx -= 1
    return tokens







