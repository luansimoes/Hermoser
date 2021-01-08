from event_set import EventSet
from section import Section
from sonic_event import SonicEvent
from piece import HermaLikePiece
import pandas as pd
import random as rd
import numpy as np
import math

INFO_MESSAGES = dict()


def random_elements(bag, size):
    output = []
    while len(output)<size:
        e = rd.choice(bag)
        if e not in [x.h for x in output]: output.append(SonicEvent(e, 80, 0))
    return output


def octave_reduction(pitch_set):
    reduction = []
    for e in pitch_set:
        if e.h%12 not in reduction:
            reduction.append(e.h%12)
    
    resp = [SonicEvent(e, 80, 0) for e in reduction]
    return resp
  
def get_interval_vector(pitch_set):
    vector = [0, 0, 0, 0, 0, 0]
    for index, event_a in enumerate(pitch_set):
        a_class = event_a.h % 12
        for event_b in pitch_set[index:]:
            b_class = event_b.h % 12

            if b_class!=a_class:
                shortest = min((a_class-b_class)%12, (b_class - a_class)%12)
                vector[shortest-1] += 1
    
    return vector

def satisfy_constraints(actual_set, other_sets, constraint):
    iv_matrix = [get_interval_vector(octave_reduction(s)) for s in other_sets]
    interval_vector = get_interval_vector(octave_reduction(actual_set))
    for vector in iv_matrix:
        diff = 0
        for i in range(len(vector)):
            diff += abs(interval_vector[i] - vector[i])
        if diff<constraint:
            return False
    return True

def random_sets_with_interval_constraints(bag=list(range(-39, 49, 1)), sizes=[26,21,25], max_value=1):
    r = EventSet([SonicEvent(x, 80, 0) for x in bag])
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
    INFO_MESSAGES['interval_vectors'] = [str(get_interval_vector(s)) for s in sets]

    return (a, b, c, r, r-a, r-b, r-c)

def print_messages():
    for key, value in INFO_MESSAGES.items():
        if type(value)==list:
            print(key + ':')
            for s in value:
                print(s)
        else:
            print(key + ": " + value)



octave = list(range(12))
two_octave = octave + [x+12 for x in octave]

octave_sets = random_sets_with_interval_constraints(octave, sizes=[5,5,5])
print_messages()
two_octave_sets = random_sets_with_interval_constraints(two_octave, sizes=[10,10,10])
print("-------------------------------------------")
print_messages()

a, b, c, r, na, nb, nc = octave_sets

sections = [
        Section(r, 0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(a, 0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(na,0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(b, 0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(nb,0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(c, 0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(nc,0.125, temporal_rule=lambda : rd.randint(1, 8)),
    ]
    
tempo=60

piece = HermaLikePiece("tests/octave_2-1.mid", tempo=tempo)
piece.set_sections(sections)
piece.run_composer(sequential=True)

a, b, c, r, na, nb, nc = two_octave_sets

sections = [
        Section(r, 0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(a, 0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(na,0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(b, 0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(nb,0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(c, 0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(nc,0.125, temporal_rule=lambda : rd.randint(1, 8)),
    ]

piece = HermaLikePiece("tests/two_octave_2-1.mid", tempo=tempo)
piece.set_sections(sections)
piece.run_composer(sequential=True)

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
            
        
        * Não consigo perceber ligação ou vínculo entre os conjuntos.
'''