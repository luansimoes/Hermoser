import numpy as np
import random as rd
from .sonic_event import SonicEvent

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