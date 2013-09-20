#!/usr/bin/python
# -*- coding: utf-8 -*-
'''Very basic formal grammar'''


class G():
    """Basic representation of a formal grammar G = (N, T, P, S).

    G(N, T, P, S) -> grammar
        N - set of nonterminal symbols
        T - set of terminal symbols
        P - set (dict) of production rules
        S - start symbol
    """
    def __init__(self, N, T, P, S):
        self.N = set(N)
        self.T = set(T)
        self.P = dict(P)
        self.S = S

    def __repr__(self):
        return '\n'.join([
            'G = (T, N, P, S)',
            '    T = {%s},' % ', '.join(t for t in self.T),
            '    N = {%s},' % ', '.join(n for n in self.N),
            '    P = {\n%s\n    },' % ',\n'.join(
            '         %s -> %s' % (p, r) for (p, r) in self.P.items()),
            '    S = %s\n' % self.S
        ])