from event_set import EventSet, DynSet
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

def random_sets_with_interval_constraints(bag=list(range(-39, 49, 1)), sizes=[26,21,25], max_value=1, base=1.265):
    r = DynSet([SonicEvent(x, 80, 0) for x in bag], base=base, mod=True)
    sets = [random_elements(bag, sizes[0])]
    for i in range(1,3,1):
        actual_set = random_elements(bag, sizes[i])
        while not satisfy_constraints(actual_set, sets, max_value):
            actual_set = random_elements(bag, sizes[i])
        sets.append(actual_set)
    a = DynSet(sets[0], base=base, mod=True)
    b = DynSet(sets[1], base=base, mod=True)
    c = DynSet(sets[2], base=base, mod=True)

    INFO_MESSAGES['sets'] = [str(r), str(a), str(r-a), str(b), str(r-b), str(c), str(r-c)]
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
two_octave_sets = random_sets_with_interval_constraints(two_octave, sizes=[10,10,10], base=2)
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
        Section(a*c,0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(a+b,0.125, temporal_rule=lambda : rd.randint(1, 8)),
    ]
    
tempo=60

piece = HermaLikePiece("tests/octave_3-2.mid", tempo=tempo)
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
        Section(a*c,0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(a+b,0.125, temporal_rule=lambda : rd.randint(1, 8)),
    ]

piece = HermaLikePiece("tests/two_octave_3-2.mid", tempo=tempo)
piece.set_sections(sections)
piece.run_composer(sequential=True)

'''
'''