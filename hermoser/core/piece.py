from midiutil import MIDIFile
from .sonic_event import SonicEvent
import music21 as m21
import operator


class HermaLikePiece:
    def __init__(self, file_name, origin=(60, 0, 0), temporal_rule=lambda:1, tempo=60):
        self.temporal_rule = temporal_rule
        self.sections = []
        self.events_list = []
        self.midi_stream = MIDIFile(2)
        self.file_name = file_name
        self.origin = origin
        self.tempo=tempo

        self.m21_stream = m21.stream.Score()

    def add_section(self, section):
        self.sections.append(section)

    def set_sections(self, sections):
        self.sections = sections

    def run_composer(self, sequential=False):
        self.base_settings()

        self.generate_vectors(seq=sequential)
        self.transform_vectors_into_midi()
        #self.midi_to_piano_roll()
        #self.transform_vectors_into_mxl()

    def transform_vectors_into_midi(self):
        print([e for e in self.events_list if e.g==0])

        self.midi_stream.addTempo(0,0,self.tempo)
        events_list = sorted(self.events_list, key=operator.attrgetter('offset'))
        for e in events_list:
            self.midi_stream.addNote(e.track, e.channel, e.h+self.origin[0], e.offset, e.u+self.origin[2], e.g+self.origin[1])
        
        with open(self.file_name+".mid", "wb") as output_file:
            self.midi_stream.writeFile(output_file)
    
    #Supõe que um elemento sonoro já é gerado pela seção com h, g, u corretos 
    #E um offset correto dentro da seção
    def generate_vectors(self, seq):
        sol_part = self.m21_stream['sol']
        
        offset = 0
        for section in self.sections:
            if len(section.event_set)!=0:
                text = m21.expressions.TextExpression('Transição')
                sol_part.insert(offset, text)

                section.generate_section()
                section.offset = offset if seq else section.offset
                events = map(lambda e: SonicEvent(e.h, e.g, e.u, offset=e.offset+section.offset, track=e.track, channel=e.channel), section.events_list)
                self.events_list += events
                offset += section.duration


    #DEPRECATED METHODS
    def midi_to_piano_roll(self):
        p = ppr.read(self.file_name+".mid")
        p.plot()

    def transform_vectors_into_mxl(self):
        treble = self.m21_stream['sol']
        bass = self.m21_stream['fa']

        events_list = sorted(self.events_list, key=operator.attrgetter('offset'))
        for e in events_list:
            note = m21.note.Note(midi=e.h+self.origin[0])
            note.volume = e.g
            note.quarterLength = e.u
            if e.h<0:
                bass.insert(e.offset, note)
                #treble.insert(e.offset, m21.note.Rest(duration=m21.duration.Duration(e.u)))
            else:
                treble.insert(e.offset, note)
                #bass.insert(e.offset, m21.note.Rest(duration=m21.duration.Duration(e.u)))
        
        self.m21_stream.write('xml', self.file_name+".xml")


    def base_settings(self):
        tempo = m21.tempo.MetronomeMark(number=self.tempo)
        self.m21_stream.insert(0, tempo)

        sol_part = m21.stream.Part(id='sol')
        sol_clef = m21.clef.TrebleClef()
        sol_part.insert(0, sol_clef)
        fa_part = m21.stream.Part(id='fa')
        fa_clef = m21.clef.BassClef()
        fa_part.insert(0, fa_clef)
        
        self.m21_stream.insert(0, sol_part)
        self.m21_stream.insert(0, fa_part)
