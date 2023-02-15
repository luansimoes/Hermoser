import numpy as np
import random as rd
from .sonic_event import SonicEvent
from math import factorial

def random_size(low, high):
    return rd.randint(low, high)

def random_elements(bag, size):
    output = []
    while len(output)<size:
        e = rd.choice(bag)
        if e not in [x.h for x in output]: output.append(SonicEvent(e, 80, 0))
    return output

def random_complete_sets(bag, sizes):
    bag_aux = [x for x in bag]
    chunks = [int(s/4) for s in sizes]

    abc = rd.randint(1, chunks[0])
    ab = rd.randint(1, 2*chunks[0]-abc)
    ac = rd.randint(1, 3*chunks[0]-(abc+ab))
    a = sizes[0] - (abc+ab+ac)

    bc = rd.randint(1, 3*chunks[1]-(abc+ab))
    b = sizes[1] - (abc+ab+bc)

    c = sizes[2] - (abc+ac+bc)


    parts = [abc, ab, ac, bc, a, b, c]
    print(parts, sum(parts), len(bag))
    part_list = []

    for p in parts:
        part = []
        for _ in range(p):
            part.append(bag_aux.pop(rd.randint(0, len(bag_aux)-1)))
        part_list.append(part)
    
    a = part_list[0]+part_list[1]+part_list[2]+part_list[4]
    b = part_list[0]+part_list[1]+part_list[3]+part_list[5]
    c = part_list[0]+part_list[2]+part_list[3]+part_list[6]

    a = [SonicEvent(e, 80, 0) for e in a]
    b = [SonicEvent(e, 80, 0) for e in b]
    c = [SonicEvent(e, 80, 0) for e in c]

    return a, b, c


def generate_partitioned_sets(bag, nr_of_main_sets):

    nr_of_subsets = 2**nr_of_main_sets

    assert nr_of_subsets <= len(bag), f'Bag should have at least many elements as the nr of subsets of {nr_of_main_sets}'

    partition = random_size_partition(len(bag), nr_of_subsets)
    all_subset_labels = list(all_subsets(nr_of_main_sets))

    pitch_partition = dict()

    bag_aux = [x for x in bag]

    for i, size in enumerate(partition):
        part = []
        for _ in range(size):
            part.append( SonicEvent( bag_aux.pop( rd.randint(0, len(bag_aux)-1) ) , 80 , 1 ))
        
        pitch_partition[all_subset_labels[i]] = part

    sets = []
    for i in range(nr_of_main_sets):

        s = []
        for label in pitch_partition.keys():

            if str(i) in label:
                p_list = pitch_partition[label]
                print(i, [x.h for x in p_list])
                s += p_list
            
        sets.append(s)


    return sets, pitch_partition


def random_size_partition(n, k):

    p = []
    n_lin = n

    for k_lin in range(k, 1, -1):

        size = np.random.binomial(n_lin, 1/k_lin)

        if size > n_lin-k_lin + 1:
            print(n_lin, k_lin, size)
            size = n_lin - k_lin + 1

        elif size == 0:
            print(n_lin, k_lin, size)
            size = 1

        p.append(size)
        n_lin -= size
    
    p.append(n_lin)
    
    rd.shuffle(p)

    return p


def all_subsets(n_sets, word = ''):

    if len(word) <= n_sets:
        yield word

        start = 0 if len(word) == 0 else int(word[-1])+1

        for x in range(start, n_sets):
            yield from all_subsets(n_sets, word + str(x))






def interval_class(a, b):
    a_class = a%12
    b_class = b%12
    return min((a_class-b_class)%12, (b_class - a_class)%12)

def get_interval_vector(pc_set):
    vector = [0, 0, 0, 0, 0, 0]
    for index, event_a in enumerate(pc_set):
        for event_b in pc_set[index:]:
            shortest = interval_class(event_a.h, event_b.h)
            if shortest!=0:
                vector[shortest-1] += 1
    
    return vector

def satisfy_constraints(sets, constraint):
    iv_matrix = [get_interval_vector(s) for s in sets]

    for i in range(len(iv_matrix)-1):
        for j in range(i+1, len(iv_matrix)):

            diff = sum([abs(iv_matrix[i][k] - iv_matrix[j][k]) for k in range(len(iv_matrix[0]))])

            if diff<constraint:
                return False
    
    return True
            
'''
def satisfy_constraints(actual_set, other_sets, constraint):
    iv_matrix = [get_interval_vector(s) for s in other_sets]
    interval_vector = get_interval_vector(actual_set)
    for vector in iv_matrix:
        diff = 0
        for i in range(len(vector)):
            diff += abs(interval_vector[i] - vector[i])
        if diff<constraint:
            return False
    return True
'''

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return round(stepper * number) / stepper

def generate_nr_samples_for_sections(lambs):
    return [np.random.default_rng().poisson(lam=lambs[i]) for i in range(len(lambs))]

def sine_func(t):
    return int(40*np.sin(np.radians(10*t)) + 80)

def abs_func(t):
    return int(100-abs(3.75*t - 60))

def prod(l):
    p = 1
    for x in l:
        p*=x
    return p

def comb(n, k):
    a, b = max(n-k, k), min(n-k, k)
    prod = n
    for v in range(n-1, a, -1):
        prod *= v
    return prod/factorial(b)