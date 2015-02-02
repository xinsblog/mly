from yacc import *

if __name__ == "__main__":
    # define the grammar
    grammar = (
            ('E', ['O', 'E', 'C', 'E']),
            ('E', ['WORD']), #list function can divide single word
            ('E', ['EPSILON']),
            ('O', ['LANGLE', 'WORD', 'RANGLE']),
            ('C', ['LANGLESLASH', 'WORD', 'RANGLE']),
            )
    # define the terminals, non-terminals and epsilon(empty symbol)
    non_terminals = ('E', 'O', 'C')
    terminals = ('WORD', 'LANGLE', 'LANGLESLASH', 'RANGLE', 'EPSILON')
    initial = 'E'
    expr = ['LANGLE', 'WORD', 'RANGLE', 'LANGLE', 'WORD', 'RANGLE', 'WORD', 'LANGLESLASH', 'WORD', 'RANGLE', 'LANGLESLASH', 'WORD', 'RANGLE']
    epsilon = 'EPSILON'


    [flag, tree] = parse(grammar, expr, initial, epsilon, terminals)
    if flag:
        print json.dumps(tree, indent=1)


