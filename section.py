from event_set import EventSet, DynSet
from sonic_event import SonicEvent
from utils import truncate
import random as rd
import numpy as np
import copy

class Section:
    def __init__(self, event_set, rhythmic_unit=1, temporal_rule=lambda: 1, offset=0):
        self.event_set = event_set
        self.ru = rhythmic_unit
        self.temporal_rule = temporal_rule
        self.events_list = []
        self.duration = 0
        self.offset = offset

    def generate_offsets(self):
        intervals = [int(self.temporal_rule()) for i in range(len(self.event_set))]
        return intervals

    def generate_section(self):
        intervals = self.generate_offsets()
        elements = copy.deepcopy(list([e for e in self.event_set]))


        for i in range(len(intervals)):
            self.events_list.append(elements.pop(rd.randint(0,len(self.event_set)-i-1)))
            self.events_list[i].assign_offset(sum(intervals[:i]) * self.ru)
            self.events_list[i].u = (sum(intervals[:i+1])-sum(intervals[:i]))*self.ru if i<len(intervals)-1 else self.events_list[i-1].u

        self.duration = (sum(intervals)*self.ru) + self.events_list[-1].u

class SetOrientedSection(Section):
    def __init__(self, event_set, rhythmic_unit, offset=0):
        super().__init__(event_set=event_set, rhythmic_unit=rhythmic_unit, offset=offset)
    
    def generate_offsets(self):
        if len(self.event_set.timepoints)==0:
            return [1]*len(self.event_set)
        else:
            return rd.choices(list(self.event_set.timepoints), k=len(self.event_set))
        


class HermaSection(Section):
    def __init__(self, event_set, length, lambda_confs=[(16,1)], offset=0, dyn=80):
        e_set = apply_dyn(event_set, dyn)
        super().__init__(e_set, offset=offset)
        self.lambda_confs = lambda_confs
        self.length = length
    
    def generate_offsets(self):
        clock = 0
        generator = np.random.default_rng()
        total_offsets = []
        for conf in self.lambda_confs:
            offsets = generator.uniform(clock, conf[0], int(conf[1]*(conf[0]-clock)))
            total_offsets+=[truncate(o, 2) for o in offsets]
            clock=conf[0]
        return total_offsets
    
    def generate_section(self):
        time_points = self.generate_offsets()
        while(len(time_points)>0):
            elements = copy.deepcopy(list(self.event_set))
            while(len(elements)>0 and len(time_points)>0):
                o = time_points.pop(rd.randint(0, len(time_points)-1))
                e = elements.pop(rd.randint(0, len(elements)-1))
                e.assign_offset(o)
                self.events_list.append(e)
        off_dict = dict()
        offsets = sorted(list(set([e.offset for e in self.events_list])))

        for i,o in enumerate(offsets):
            off_dict[o] = offsets[i+1]-offsets[i] if i<len(offsets)-1 else self.length-offsets[i]

        for i,e in enumerate(self.events_list):
            e.u = truncate(off_dict[e.offset], 2)
            
'''
PenuriaSection usa uma função de dinâmica para gerar as intensidades de cada evento sonoro.
- Função de Dinâmica
- Distribuição Exponencial com parâmetro lambda
- Sorteia intervalos de tempo e eventos sonoros separadamente para combinar os timepoints
'''
class PenuriaSection(Section):
    def __init__(self, event_set, din_func, length, rhythmic_unit=1,
                lamb=1, relative_offset=0, offset=0):
        super().__init__(event_set, rhythmic_unit=rhythmic_unit, offset=offset)
        self.din_func = din_func
        self.length = length/rhythmic_unit
        self.rel_offset = relative_offset
        self.lamb = lamb*rhythmic_unit
    
    def generate_offsets(self):
        intervals = []
        generator = np.random.default_rng()
        generated = 0
        while sum(intervals)+generated<self.length:
            intervals.append(generated)
            generated = int(generator.exponential(scale=1/self.lamb))
        return intervals
    
    def generate_section(self):
        intervals = self.generate_offsets()
        elements = list([e for e in self.event_set])

        for i in range(len(intervals)):
            e = rd.choice(elements)
            off = int(sum(intervals[:i+1]))*self.ru
            event = SonicEvent(e.h, self.din_func(off+self.rel_offset), e.u)
            event.assign_offset(off)
            self.events_list.append(event)

            
        self.duration = sum(intervals) + self.events_list[-1].u

def apply_dyn(e_set, dyn):
    e_list = copy.deepcopy(e_set.list)
    for e in e_list:
        e.g = dyn
    return EventSet(e_list)
