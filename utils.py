import copy
import numpy as np
from sonic_event import SonicEvent

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


'''
def octave_herma_example(sections, filename):
    tempo = 60
    #tax = tempo/60

    piece = HermaLikePiece(filename, tempo=tempo)
    piece.set_sections(sections)
    piece.run_composer(sequential=True)
'''