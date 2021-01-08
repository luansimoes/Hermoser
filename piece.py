from midiutil import MIDIFile
from sonic_event import SonicEvent
import operator


class HermaLikePiece:
    def __init__(self, file_name, origin=(60, 0, 0), temporal_rule=lambda:1, tempo=60):
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
        print([e for e in self.events_list if e.g==0])

        self.midi_stream.addTempo(0,0,self.tempo)
        events_list = sorted(self.events_list, key=operator.attrgetter('offset'))
        for e in events_list:
            print(e.g)
            self.midi_stream.addNote(e.track, e.channel, e.h+self.origin[0], e.offset, e.u+self.origin[2], e.g+self.origin[1])
        
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
            events = map(lambda e: SonicEvent(e.h, e.g, e.u, offset=e.offset+section.offset, track=e.track, channel=e.channel), section.events_list)
            self.events_list += events
            offset += section.duration