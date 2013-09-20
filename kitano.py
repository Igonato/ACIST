#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Lab1.py 
Graph based evolutionary generated neural networks (see Hiroaki Kitano paper)
"""
import random
import itertools
import numpy as np
from grammar import G


VARIABLE_PART_LENGTH = 79 # 16 rules -> 15*5 + 4 = 79 symbols
DERIVATION_DEPTH = 3 # we will end up with 8x8 0 and 1 matrix
PROPAGANATIONS_COUNT = 10
GENERATIONS_COUNT = 10
POPULATION_SIZE = 20
F = lambda A, B, C, D: (A or not B or C) is D
F_ARGS_COUNT = F.func_code.co_varnames


base_grammar = G(
    N = {
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 
        'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p'
    },
    T = {'0', '1'},
    P = {
        'a': '0000',
        'b': '0001',
        'c': '0010',
        'd': '0011',
        'e': '0100',
        'f': '0101',
        'g': '0110',
        'h': '0111',
        'i': '1000',
        'j': '1001',
        'k': '1010',
        'l': '1011',
        'm': '1100',
        'n': '1101',
        'o': '1110',
        'p': '1111',
        
        '1': '1111',
    },
    S = 'S'
)

kitano_nonterminals = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]

kitano_preterminals = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
    'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p'
]

variable_part_symbols = kitano_nonterminals + kitano_preterminals

def get_random_chromosome(lenght=VARIABLE_PART_LENGTH, 
                          symbols=variable_part_symbols):
    return ''.join(
        random.choice(symbols) 
        for _ in range(lenght)
    )

def grammar_from_chromosome(chromosome):
    p = {'S': chromosome[:4]}
    p.update({
        chromosome[i]: chromosome[i+1:i+5] 
        for i in range(4, len(chromosome), 5)
        if chromosome[i] in kitano_nonterminals
    })
    p.update(base_grammar.P)
    return G(base_grammar.N, base_grammar.T, p, base_grammar.S)

def derivation(grammar):
    steps = [np.array([['S']])]
    for i in range(1, DERIVATION_DEPTH + 1):
        step = np.ndarray(shape=[2**i, 2**i], dtype='|S1')
        n = 2**(i-1)
        for j in range(n):
            for k in range(n):
                symbol = steps[-1][j, k]
                rule = grammar.P.get(symbol, '0000')
                if i == DERIVATION_DEPTH and symbol in kitano_nonterminals:
                    rule = '0000'                    
                for x in range(4):
                    step[2*j + x/2, 2*k + x%2] = rule[x]
        steps.append(step)
    return steps

def matrix_triangulation(adjacency_matrix):
    n = 2**DERIVATION_DEPTH
    for i in range(n):
        for j in range(i, n):
            adjacency_matrix[j, i] = '0'

    return adjacency_matrix

def matrix_to_dot(adjacency_matrix):
    dotdata = 'digraph G {\n'
    for i in range(2**DERIVATION_DEPTH):
        for j in range(i, 2**DERIVATION_DEPTH):
            if adjacency_matrix[i, j] == '1':
                dotdata += '%i -> %i;\n' % (i, j)



    return dotdata + '}'