from herma import EventSet, SonicEvent, Section, PenuriaSection, HermaSection, HermaLikePiece, get_vector_sets, apply_dyn, octave_herma_example
import pandas as pd
import random as rd
import numpy as np
import math

INFO_MESSAGES = dict()


def random_elements(bag, size):
    output = []
    while len(output)<size:
        e = rd.choice(bag)
        if e not in [x.vector[0] for x in output]: output.append(SonicEvent([e, 80, 0]))
    return output
  
def get_p_interval_vector(pitch_set, n_elems=88):
    vector = [0 for i in range(n_elems)]
    for index, event_a in enumerate(pitch_set):
        a_real = event_a.vector[0]
        for event_b in pitch_set[index:]:
            b_real = event_b.vector[0]
            if b_real!=a_real:
                interval = abs(a_real-b_real)
                vector[interval-1] += 1
    return vector

def satisfy_constraints(actual_set, other_sets, constraint):
    iv_matrix = [get_p_interval_vector(s, 88) for s in other_sets]
    interval_vector = get_p_interval_vector(actual_set, 88)
    for vector in iv_matrix:
        diff = 0
        for i in range(len(vector)):
            diff += abs(interval_vector[i] - vector[i])
        if diff<constraint:
            return False
    return True

def random_sets_with_interval_constraints(bag=list(range(-39, 49, 1)), sizes=[26,21,25], max_value=30):
    r = EventSet([SonicEvent([x, 80, 0]) for x in bag])
    sets = [random_elements(bag, sizes[0])]
    for i in range(1,3,1):
        actual_set = random_elements(bag, sizes[i])
        while not satisfy_constraints(actual_set, sets, max_value):
            actual_set = random_elements(bag, sizes[i])
        sets.append(actual_set)
    a = EventSet(sets[0])
    b = EventSet(sets[1])
    c = EventSet(sets[2])

    INFO_MESSAGES['sets'] = [str(a), str(b), str(c)]
    INFO_MESSAGES['interval_vectors'] = [str(get_p_interval_vector(s)) for s in sets]

    return (a, b, c, r, r-a, r-b, r-c)

def print_messages():
    for key, value in INFO_MESSAGES.items():
        if type(value)==list:
            print(key + ':')
            for s in value:
                print(s)
        else:
            print(key + ": " + value)



herma_like_sets = random_sets_with_interval_constraints()
print_messages()

a, b, c, r, na, nb, nc = herma_like_sets

sections = [
        Section(r, 0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(a, 0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(na,0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(b, 0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(nb,0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(c, 0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(nc,0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(a, 0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(b, 0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(c, 0.125, temporal_rule=lambda : rd.randint(1, 8)),
    ]

octave_herma_example(sections, "tests/herma_like_2-1.mid")

'''
    1° Execução
    Anotações:
        - A: 0, 3, 6, 8, 11 / [1, 1, 3, 2, 2, 1]
            - Apresentação da seção A conta com uma tríade de Ab seguida de uma tríade de B.
            - Na seção ~A, aparece logo de cara um acorde maior de Bb depois D, depois A7.
        - B: 7, 8, 9, 10, 11 / [4, 3, 2, 1, 0, 0]
            - Apesar do cromatismo aparente, a ordem das notas não cria uma atmosfera cromática na seção B.
            - Na seção ~B, no entanto, essa atmosfera aparece.
        - C: 1, 4, 5, 8, 9 / [2, 0, 2, 4, 2, 0]
            - Uma tríade de Abm. Logo após, em ~C, aparece uma tríade de Am.
        
        * Não consigo perceber ligação ou vínculo entre os conjuntos.
'''