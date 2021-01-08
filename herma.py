'''
(h, u) => sorteio no tempo gera g e t.

seções se alternam

'''

from midiutil import MIDIFile
import numpy as np
import pandas as pd
import random as rd
import math
import music21 as m21
import operator
import copy
from collections import UserList

class HermaLikePiece:
    def __init__(self, file_name, origin=(60, 40, 0), temporal_rule=lambda:1, tempo=60):
        self.temporal_rule = temporal_rule
        self.sections = []
        self.events_list = []
        self.midi_stream = MIDIFile(1)
        self.file_name = file_name
        self.origin = origin
        self.tempo=tempo

    def add_section(self, section):
        self.sections.append(section)

    def set_sections(self, sections):
        self.sections = sections

    def run_composer(self, sequential=False):
        self.generate_vectors(seq=sequential)
        self.transform_vectors_into_midi()

    def transform_vectors_into_midi(self):
        print([e for e in self.events_list if e.vector[1]==0])

        self.midi_stream.addTempo(0,0,self.tempo)
        events_list = sorted(self.events_list, key=operator.attrgetter('offset'))
        for e in events_list:
            self.midi_stream.addNote(e.track, e.channel, e.vector[0]+self.origin[0], e.offset, e.vector[2]+self.origin[2], e.vector[1]+self.origin[1])
        
        with open(self.file_name, "wb") as output_file:
            self.midi_stream.writeFile(output_file)
    
    #Supõe que um elemento sonoro já é gerado pela seção com h, g, u corretos 
    #E um offset correto dentro da seção
    def generate_vectors(self, seq):
        offset = 0
        for section in self.sections:
            section.generate_section()
            print(len(section.events_list))
            section.offset = offset if seq else section.offset
            events = map(lambda e: SonicEvent(e.vector, offset=e.offset+section.offset, track=e.track, channel=e.channel), section.events_list)
            self.events_list += events
            offset += section.duration


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
            self.events_list[i].vector[2] = (sum(intervals[:i+1])-sum(intervals[:i]))*self.ru if i<len(intervals)-1 else self.events_list[i-1].vector[2]
            #print(self.events_list[i].vector[2])

        self.duration = (sum(intervals)*self.ru) + self.events_list[-1].vector[2]

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
            e.vector[2] = truncate(off_dict[e.offset], 2)
            
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
            event = SonicEvent([e.vector[0], self.din_func(off+self.rel_offset), e.vector[2]])
            event.assign_offset(off)
            self.events_list.append(event)

            
        self.duration = sum(intervals) + self.events_list[-1].vector[2]

class EventSet():
    def __init__(self, event_list):
        self.list = list()
        self.dyn = event_list[0].vector[1]
        self.create_set(event_list)
    
    def create_set(self, event_list):
        #itera sobre todos os eventos e chama contains - O(n^2) (na vdd contains é uma pa)
        for e in event_list:
            if e not in self:
                self.list.append(e)
    
    def __iter__(self):
        return (e for e in self.list)
        
    def __contains__(self, item):
        #O(m) - qtd de itens diferentes  na lista inicial
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
        message = "**********EVENT SET***********\n"
        return message + '\n'.join([e.__str__() for e in self])

#TODO: change vector representation to h, g, u attributes
class SonicEvent:
    def __init__(self, vector, offset=0, track=0, channel=0):
        self.vector = vector
        self.offset = offset
        self.track = track
        self.channel = channel

    def assign_offset(self, o):
        self.offset = o
    
    def __eq__(self, other):
        return (self.vector[0]==other.vector[0])and(self.vector[1]==other.vector[1])and(self.vector[2]==other.vector[2])
    
    def __str__(self):
        return "Sonic Event: \n<h,g,u>: " + str(self.vector) +'\nOffset: ' + str(self.offset) + '\n'

def apply_dyn(e_set, dyn):
    e_list = copy.deepcopy(e_set.list)
    for e in e_list:
        e.vector[1] = dyn
    return EventSet(e_list)

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return round(stepper * number) / stepper

def long_to_dur(lon, median):
	return round((lon-median)/72)

def lat_to_pitch(lat, median):
    h_i = int((lat-median)/3)
    return h_i

def translate_coords(row, lat_median, lon_median):
    h = lat_to_pitch(row['latitude'], lat_median)
    u = long_to_dur(row['longitude'], lon_median)
    event = SonicEvent([h, 0, u])
    return event

def get_vector_sets(df, param):
	lat_median = df["latitude"].median()
	lon_median = df["longitude"].median()


	north = EventSet([translate_coords(row, lat_median, lon_median) for index, row in df.loc[df["latitude"]>lat_median].iterrows() if row[param]!=0])
	east = EventSet([translate_coords(row, lat_median, lon_median) for index, row in df.loc[df["longitude"]>lon_median].iterrows() if row[param]!=0])

	mean_param = df[param].mean()
	poor = EventSet([translate_coords(row, lat_median, lon_median) for index, row in df.loc[df[param]<mean_param].iterrows() if row[param]!=0])

	r = EventSet(translate_coords(row, lat_median, lon_median) for index, row in df.iterrows() if row[param]!=0)
	return (north, east, poor, r)

def generate_nr_samples_for_sections(lambs):
    return [np.random.default_rng().poisson(lam=lambs[i]) for i in range(len(lambs))]

def sine_func(t):
    return int(40*math.sin(math.radians(10*t)) + 80)

def abs_func(t):
    return int(100-abs(3.75*t - 60))
    

    #s = m21.converter.parse('penia_1_test.mid')
    #s.write('xml', 'penia_1_test.xml')

def midi_from_list(midi_list, file_name):
    tempo = 60 #matching seconds with beats
    output_midi = MIDIFile(1)
    output_midi.addTempo(0,0,tempo)
    time = 0
    for v in midi_list:
        output_midi.addNote(0,0,v[0]+60, time, 2**(v[1]), 60)
        time+=2**(v[1])
    
    with open(file_name, "wb") as output_file:
        output_midi.writeFile(output_file) 

def octave_herma_example(sections, filename):
    tempo = 60
    #tax = tempo/60

    piece = HermaLikePiece(filename, tempo=tempo)
    piece.set_sections(sections)
    piece.run_composer(sequential=True)