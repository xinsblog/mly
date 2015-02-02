from lex import *

if __name__ == "__main__":
    # generate rules from test.l, and write them in test.l.out
    gen_rules('test/test.l', 'test/test.l.out')
    # import rules from test.l.out
    rules = import_rules('test/test.l.out')
    # detect token from test.c
    tokens = analyze(rules, 'test/test.c')
    # print the tokens
    for t in tokens:
        t.show()

