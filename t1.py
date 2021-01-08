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

def random_sets(bag=list(range(-39, 49, 1)), sizes=[26,21,25]):
    r = EventSet([SonicEvent(x, 80, 0) for x in bag])
    a = EventSet([SonicEvent(rd.choice(bag), 80, 0) for i in range(sizes[0])])
    b = EventSet([SonicEvent(rd.choice(bag), 80, 0) for i in range(sizes[1])])
    c = EventSet([SonicEvent(rd.choice(bag), 80, 0) for i in range(sizes[2])])

    na = r-a
    nb = r-b
    nc = r-c

    INFO_MESSAGES['sets'] = [a, b, c]

    return (a, b, c, r, na, nb, nc)

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

octave_sets = random_sets(octave, sizes=[5,5,5])
print_messages()
two_octave_sets = random_sets(two_octave, sizes=[10,10,10])
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


tempo = 60
#tax = tempo/60

piece = HermaLikePiece("tests/octave_1-2.mid", tempo=tempo)
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


piece = HermaLikePiece("tests/two_octave_1-2.mid", tempo=tempo)
piece.set_sections(sections)
piece.run_composer(sequential=True)

'''
    1° Execução
    Anotações:
        - A: 1, 7, 8, 10, 11 / [2, 2, 3, 1, 1, 1]
            - Apresentação de A soa como uma tríade G°, com uma suspensão do B.
            - O ritmo é o que reforça isso - tem importância na percepção do conjunto.
        - B: 2, 6, 9 / [0, 0, 1, 1, 1, 0]
            - Uma tríade de ré maior.
        - C: 3, 8, 11 / [0, 0, 1, 1, 1, 0]
            - Uma tríade de Abm. Logo após, em ~C, aparece uma tríade de Am.
        
        * Por algum motivo, a sustentação do Bb nas seções A e C cria uma identidade entre eles, 
            meu ouvido pede por um repouso no lá, mesmo quando escuto o acorde de Abm na seção C.
            A interseção em Ab e B cria uma unidade entre os próprios conjuntos, talvez por serem pequenos demais.
            A aleatoriedade ainda dita muito as características da composição final.


'''