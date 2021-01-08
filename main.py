from herma import EventSet, SonicEvent, Section, PenuriaSection, HermaSection, HermaLikePiece, get_vector_sets, apply_dyn, octave_herma_example
import pandas as pd
import random as rd
import numpy as np
import math

INFO_MESSAGES = dict()


def herma_example():
    tempo = 120
    tax = tempo/60

    sets = [
        [ -31, -29, -27, -22, -21, -19, -13, -12, -11, -5, -4,
            2, 5, 6, 7, 17, 18, 19, 21, 22, 26, 28, 33, 35, 36, 38],
        [ -38, -35, -32, -18, -16, -12, -11, -8,
            2, 5, 6, 7, 15, 18, 21, 22, 23, 35, 40, 44, 45], 
        [-38, -35, -23, -22, -21, -13, -12, -9, -8, -2, -1,
        5, 6, 7, 15, 20, 22, 23, 25, 28, 36, 45, 46, 47, 48]
        ]

    event_sets = [[SonicEvent([e, 80, 0]) for e in s] for s in sets]

    a, b, c, r = (EventSet(event_sets[0]), EventSet(event_sets[1]), EventSet(event_sets[2]), EventSet(event_sets[0]+event_sets[1]+event_sets[2]))

    na = r-a
    nb = r-b
    nc = r-c

    sections = [
        HermaSection(r, 36.5*tax, [(14*tax,1.73/tax), (23*tax,2.8/tax), (28.5*tax,4.53/tax), (32*tax,7.32/tax), (34.5*tax,11.8/tax), (36*tax,19/tax), (36.5*tax,31/tax)], offset=0, dyn=40),
        HermaSection(a, 46*tax, [(46*tax, 0.8/tax)], offset=36.5*tax, dyn=100),
        HermaSection(a, 16*tax, [(16*tax, 3.3/tax)], offset=45*tax, dyn=20),
        HermaSection(a, 12.5*tax, [(12.5*tax, 5/tax)], offset=70*tax, dyn=20),
        HermaSection(na, 26*tax, [(26*tax, 10/tax)], offset=100*tax, dyn=100),
        HermaSection(b, 14*tax, [(14*tax, 1.76/tax)], offset=126*tax, dyn=80),
        HermaSection(b, 14*tax, [(14*tax, 3.3/tax)], offset=128*tax, dyn=20),
        HermaSection(b, 1*tax, [(1*tax, 5/tax)], offset=134*tax, dyn=20),
        HermaSection(b, 24*tax, [(24*tax, 5/tax)], offset=138*tax, dyn=20),
        HermaSection(b, 19*tax, [(19*tax, 1.76/tax)], offset=150*tax, dyn=80),
        HermaSection(nb, 22*tax, [(22*tax, 10/tax)], offset=182*tax, dyn=100),
        HermaSection(c, 18*tax, [(18*tax, 2.5/tax)], offset=208*tax, dyn=20),
        HermaSection(c, 10*tax, [(10*tax, 5/tax)], offset=212*tax, dyn=100),
        HermaSection(nc, 34*tax, [(34*tax, 9/tax)], offset=216*tax, dyn=100),
        HermaSection(a*b, 6*tax, [(6*tax, 0.8/tax)], offset=256*tax, dyn=20),
        HermaSection(b*c, 4*tax, [(4*tax, 0.8/tax)], offset=270*tax, dyn=80),
        HermaSection(a*b, 4*tax, [(4*tax, 10/tax)], offset=256*tax, dyn=20),
        HermaSection(na*nb + a*b, 12*tax, [(12*tax, 20/tax)], offset=278*tax, dyn=20),
        HermaSection(b*c, 2*tax, [(2*tax, 5/tax)], offset=285*tax, dyn=80),
        HermaSection(a*b*c, 4*tax, [(4*tax, 6/tax)], offset=287*tax, dyn=120),
        HermaSection(na*nb + a*b, 4*tax, [(4*tax, 20/tax)], offset=294*tax, dyn=20),
        HermaSection(na*nb*c, 6*tax, [(6*tax, 6/tax)], offset=296*tax, dyn=120),
        HermaSection((a*b+na*nb)*c, 8*tax, [(8*tax, 12/tax)], offset=298*tax, dyn=100),
        HermaSection(b*c, 2*tax, [(2*tax, 6/tax)], offset=300*tax, dyn=80),
        HermaSection(nb*nc, 8*tax, [(8*tax, 10/tax)], offset=302*tax, dyn=80),
        HermaSection(r - (na*nb + a*b), 12*tax, [(12*tax, 1/tax)], offset=306*tax, dyn=20),
        HermaSection(a*nb*nc, 2*tax, [(2*tax, 3/tax)], offset=313*tax, dyn=120),
        HermaSection(nc*(r-(na*nb + a*b)), 17*tax, [(17*tax, 3/tax)], offset=318*tax, dyn=20),
        HermaSection((a*b+na*nb)*c, 2*tax, [(2*tax, 6/tax)], offset=322*tax, dyn=100),
        HermaSection(a*nb*nc, 2*tax, [(2*tax, 3/tax)], offset=338*tax, dyn=120),
        HermaSection(na*nc, 10*tax, [(10*tax, 10/tax)], offset=340*tax, dyn=80),
        HermaSection(nc*(r-(na*nb + a*b)), 2*tax, [(2*tax, 5/tax)], offset=344*tax, dyn=20),
        HermaSection(a*nb*nc, 2*tax, [(2*tax, 1/tax)], offset=346*tax, dyn=120),
        HermaSection(nc*(r-(na*nb + a*b)), 8*tax, [(8*tax, 1/tax)], offset=350*tax, dyn=20),
        HermaSection((a*b+na*nb)*c, 2*tax, [(2*tax, 10/tax)], offset=354*tax, dyn=100),
        HermaSection(na*nc, 16*tax, [(16*tax, 5/tax)], offset=362*tax, dyn=80),
        HermaSection(a*nb*nc, 2*tax, [(2*tax, 5/tax)], offset=366*tax, dyn=120),
        HermaSection(na*b*nc, 2*tax, [(2*tax, 20/tax)], offset=376*tax, dyn=20),
        HermaSection(nc*(r-(na*nb + a*b)), 12*tax, [(12*tax, 1/tax)], offset=382*tax, dyn=20),
        HermaSection(c*(a*b + na*nb), 2*tax, [(2*tax, 3/tax)], offset=386*tax, dyn=100),
        HermaSection(a*nb*nc, 2*tax, [(2*tax, 1/tax)], offset=390*tax, dyn=120),
        HermaSection(na*b*nc, 2*tax, [(2*tax, 3/tax)], offset=394*tax, dyn=120),
        HermaSection(nc*(r-(na*nb + a*b)), 5*tax, [(5*tax, 6/tax)], offset=398*tax, dyn=100),
        HermaSection(a*b*c + a*nb*nc + na*b*nc + na*nb*c, 11*tax, [(11*tax, 20/tax)], offset=414*tax, dyn=120),
    ]

    piece = HermaLikePiece("herma_like.mid", tempo=tempo)
    piece.set_sections(sections)
    piece.run_composer()

def general_example():
    r,a,b,c = (EventSet([]), EventSet([]), EventSet([]), EventSet([])) 

    resolution = 0.25
    sections = [
    Section(r, rhythmic_unit=resolution),
    Section(a, rhythmic_unit=resolution, offset=len(r)*resolution),
    Section(b, rhythmic_unit=resolution, offset=resolution*(len(r)+len(a))),
    Section(c, rhythmic_unit=resolution, offset=resolution*(len(r)+len(a)+len(b))),
    ]

    piece = HermaLikePiece("general_piece.mid")
    piece.set_sections(sections)
    piece.run_composer()

def penuria_example():
    df_gdp = pd.read_csv('tables/gdp.csv', index_col="Country Name")
    df_coord = pd.read_csv('tables/countries.csv', index_col="name")
    df = df_gdp.join(df_coord).fillna(0)

    a,b,c,r = get_vector_sets(df, "GDP per capita")
    na = r-a
    nb = r-b
    nc = r-c

    sections = [
        PenuriaSection(r, lambda t: 40, 32, rhythmic_unit=resolution+0.25, lamb=1.5),

        PenuriaSection(na*b, lambda t: int(100-abs(2.5*t-40)), 8, lamb=1.5, offset=32, rhythmic_unit=resolution),
        PenuriaSection(na*(b+c), lambda t: int(100-abs(2.5*t-40)), 8, lamb=1.2, offset=40, rhythmic_unit=resolution, relative_offset=8),
        PenuriaSection(na*nb*nc, lambda t: int(100-abs(2.5*t-40)), 16, lamb=1.4, offset=48, rhythmic_unit=resolution, relative_offset=16),
        PenuriaSection(nb*nc, lambda t: int(100-abs(2.5*t-40)), 8, lamb=2, offset=56, rhythmic_unit=resolution, relative_offset=24),
        
        PenuriaSection(nb+a, lambda t: int(((60/(16**2))*t*t) + 60), 4, lamb=2, offset=64, rhythmic_unit=resolution, relative_offset=0),
        PenuriaSection(a+(nb*nc), lambda t: int(((60/(16**2))*t*t) + 60), 4, lamb=2.5, offset=68, rhythmic_unit=resolution, relative_offset=4),
        PenuriaSection(a+b+c, lambda t: int(((60/(16**2))*t*t) + 60), 4, lamb=3, offset=72, rhythmic_unit=resolution, relative_offset=8),
        PenuriaSection(b+c, lambda t: int(((60/(16**2))*t*t) + 60), 4, lamb=3.5, offset=76, rhythmic_unit=resolution, relative_offset=12),

        PenuriaSection(b*c, lambda t: 120, 16, lamb=0.5, offset=80, rhythmic_unit=1, relative_offset=0),
        PenuriaSection(c, lambda t: int(20*math.sin((math.pi/8)*t) + 60), 16, lamb=1.5, offset=96, rhythmic_unit=1, relative_offset=0),
        PenuriaSection(nc, lambda t: 120, 8, lamb=4, offset=112,rhythmic_unit=resolution, relative_offset=0),  
    ]

    piece = HermaLikePiece("penuria_like.mid")
    piece.set_sections(sections)
    piece.run_composer()

def generate_dyn_sets(sets):
    factors = [2,3,5,7,11,13,17,19,23,29,31,37]
    output = [[factors[e.vector[0]] for e in s] for s in sets]
    return output

def random_sets(bag=list(range(-39, 49, 1)), sizes=[30,30,30]):
    r = EventSet([SonicEvent([x, 80, 0]) for x in bag])
    a = EventSet([SonicEvent([rd.choice(bag), 80, 0]) for i in range(sizes[0])])
    b = EventSet([SonicEvent([rd.choice(bag), 80, 0]) for i in range(sizes[1])])
    c = EventSet([SonicEvent([rd.choice(bag), 80, 0]) for i in range(sizes[2])])

    na = r-a
    nb = r-b
    nc = r-c

    return (a, b, c, r, na, nb, nc)

def octave_reduction(pitch_set):
    reduction = []
    for e in pitch_set:
        if e.vector[0]%12 not in reduction:
            reduction.append(e.vector[0]%12)
    
    resp = [SonicEvent([e, 80, 0]) for e in reduction]
    return resp
        
def get_interval_vector(pitch_set):
    vector = [0, 0, 0, 0, 0, 0]
    for index, event_a in enumerate(pitch_set):
        a_class = event_a.vector[0] % 12
        for event_b in pitch_set[index:]:
            b_class = event_b.vector[0] % 12

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

def random_elements(bag, size):
    output = []
    while len(output)<size:
        e = rd.choice(bag)
        if e not in [x.vector[0] for x in output]: output.append(SonicEvent([e, 80, 0]))
    return output

def random_sets_with_interval_constraints(bag=list(range(-39, 49, 1)), sizes=[26,21,25], max_value=1):
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

two_octave_sets = random_sets_with_interval_constraints(two_octave, [8, 8, 8], max_value=6)
octave_sets = random_sets_with_interval_constraints(bag=octave, sizes=[5, 5, 5], max_value=6)

a, b, c, r, na, nb, nc = octave_sets

'''
dyn_sets = generate_dyn_sets(octave_sets)
tax = 120/np.prod(dyn_sets[3])
real_dyn = [tax*np.prod(d) for d in dyn_sets]
'''


'''
sections = [
        Section(apply_dyn(r, real_dyn[3]), 0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(apply_dyn(a, real_dyn[0]), 0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(apply_dyn(na, real_dyn[4]),0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(apply_dyn(b, real_dyn[1]), 0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(apply_dyn(nb, real_dyn[5]),0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(apply_dyn(c, real_dyn[2]), 0.125, temporal_rule=lambda : rd.randint(1, 8)),
        Section(apply_dyn(nc, real_dyn[6]),0.125, temporal_rule=lambda : rd.randint(1, 8)),
    ]

octave_herma_example(sections, "tests/octave_3-1.mid")
print_messages()
'''

'''
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

octave_herma_example(sections, "tests/two_octave_2-11.mid")
'''

'''
Teste 1:
    Conjuntos: Correspondentes à apresentação da Herma, mas com teclas escolhidas aleatoriamente num domínio menor.
    Durações (lambdas): Sempre em 1.5, não há alteração na geração de timepoints
    Dinâmicas: Constantes em 80, f.

Teste 2:
    Conjuntos: Selecionados a partir de uma qualidade específica. 
        2.1. Pentacordes com garantia de vetor intervalar com diff>6
    Durações: Aleatorizadas em uma unidade rítmica
    Dinâmicas: Constantes em 80, f.

'''