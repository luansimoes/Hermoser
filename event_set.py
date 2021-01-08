import numpy as np
from utils import prod
import math
import copy

class EventSet():
    def __init__(self, event_list):
        self.list = list()
        self.dyn = event_list[0].g
        self.create_set(event_list)
    
    def create_set(self, event_list):
        for e in event_list:
            if e not in self:
                self.list.append(e)
    
    def __iter__(self):
        return (e for e in self.list)
        
    def __contains__(self, item):
        for e in self.list:
            if e==item:
                return True
        return False
    
    def __len__(self):
        return len(self.list)
    
    def __add__(self, o):
        return EventSet(self.list+[e for e in o.list if e not in self])
    
    def __sub__(self, o):
        return EventSet([e for e in self if e not in o])
    
    def __mul__(self, o):
        return EventSet([e for e in self if e in o])
    
    def __str__(self):
        message = "**********EVENT SET - DYN: "+str(self.dyn)+" ***********\n"
        return message + '\n'.join([e.__str__() for e in self])

class DynSet(EventSet):
    def __init__(self, event_list, base=2, dyn_vector=set(), mod=False):
        self.base = base
        self.dyn_vector = dyn_vector
        self.mod=mod
        self.list = list()
        self.create_set(event_list)
        self.apply_dyn(mod)
    
    def apply_dyn(self, mod):
        prime_list = []
        for x in range(2,128):
            prime = True
            for y in range(2, int(np.sqrt(x)+1)):
                if x%y==0:
                    prime = False
            if prime:
                prime_list.append(x)
        
        i_list = [e.h for e in self.list] if len(self.dyn_vector)==0 else self.dyn_vector
        indexed_primes = [prime_list[i] for i in i_list]

        if not mod:
            real_dyn = int(math.log(prod(indexed_primes), self.base))
        else:
            real_dyn = 30 + 6*(prod(indexed_primes)%15)

        for e in self.list:
            e.g = real_dyn

        self.dyn=real_dyn
    
    def __add__(self, o):
        return DynSet(copy.deepcopy(self.list+[e for e in o.list if e not in self]), base=self.base, dyn_vector=self.dyn_vector.union(o.dyn_vector), mod=self.mod)

    def __sub__(self, o):
        return DynSet(copy.deepcopy([e for e in self if e not in o]), base=self.base, dyn_vector=set([i for i in self.dyn_vector if i not in o.dyn_vector]), mod=self.mod)

    def __mul__(self, o):
        return DynSet(copy.deepcopy([e for e in self if e in o]), base=self.base, dyn_vector=self.dyn_vector.intersection(o.dyn_vector), mod=self.mod)