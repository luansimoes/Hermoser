import numpy as np
import random as rd
from .sonic_event import SonicEvent
from math import factorial

def random_size(low, high):
    return rd.randint(low, high)

def generate_partitioned_sets(bag, nr_of_main_sets, event = True):
    """
    Partitions a given bag of elements into a number of main sets, with each possible combination of unions, intersections and complements of these main sets being non-empty.
    Args:
        bag (list): The list of elements to partition.
        nr_of_main_sets (int): The number of main sets to partition the bag into.
        event (bool, optional): If True, wraps each element in a SonicEvent object; otherwise, uses the raw element. Defaults to True.
    Returns:
        tuple:
            - sets (list of lists): A list containing the main sets, each as a list of elements.
            - el_partition (dict): A dictionary mapping region labels (as strings) to lists of elements assigned to each region.
    Raises:
        AssertionError: If the number of possible subsets (2**nr_of_main_sets) exceeds the number of elements in the bag.
    Notes:
        - The function randomly partitions the bag into subsets, then distributes elements to main sets based on subset labels.
        - Subset labels are generated using all possible combinations of main set indices.
    """

    nr_of_regions = 2**nr_of_main_sets

    assert nr_of_regions <= len(bag), f'Bag should have at least many elements as the nr of disjoint regions in the venn diagram of {nr_of_main_sets}'

    regions = generate_random_sized_partitions(bag, nr_of_regions)
    labels = list(all_disj_region_labels(nr_of_main_sets))

    np.random.shuffle(labels)

    if event:
        mapping = lambda x: SonicEvent(x, 80, 1)
        regions = [list(map(mapping, region)) for region in regions]

    el_partition = dict(zip(labels, regions))

    sets = []
    for i in range(nr_of_main_sets):

        s = []
        for label in el_partition.keys():

            if str(i) in label:
                p_list = el_partition[label]
                s.extend(p_list)
            
        sets.append(s)

    return sets, el_partition

def generate_random_sized_partitions(bag, nr_of_regions):
    '''
    Randomly chooses the regions from the given bag, using binomial distribution in the choice of the sizes of the sets.
    Args:
        - bag (list): the pitches to be partitioned
        - nr_of_regions: the number of regions that must be chosen.
    Returns:
        - a list of lists, having the chosen sets.
    '''
    bag_copy = [x for x in bag] 
    rd.shuffle(bag_copy)

    regions = []
    nr_remaining_pitches = len(bag_copy) - nr_of_regions

    total_size = 0
    for nr_remaining_regions in range(nr_of_regions, 0, -1):

        region_size = np.random.binomial(nr_remaining_pitches, 1/nr_remaining_regions) + 1 #includes the mandatory pitch
        regions.append(bag_copy[total_size:total_size+region_size]) 
        total_size += region_size
        nr_remaining_pitches -= (region_size-1) #excludes the mandatory pitch
    
    return regions
        

'''
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
'''


def all_disj_region_labels(n_sets, word = ''):
    """
    Recursively yields the labels for each disjoint region of the venn diagram for the given number of sets.
    Args:
        - n_sets (int): The number of sets in the venn diagram.
        - word (str, optional): the current label.
    Returns:
        - generator object with every possible label (str)
    """
    if len(word) <= n_sets:
        yield word

        start = 0 if len(word) == 0 else int(word[-1])+1

        for x in range(start, n_sets):
            yield from all_disj_region_labels(n_sets, word + str(x))






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