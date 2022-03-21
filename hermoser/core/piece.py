from midiutil import MIDIFile
from .sonic_event import SonicEvent
import music21 as m21
from scamp import Session, wait
import operator

# TODO : Fazer com SCAMP
# TODO : Mudar vetor de origem
class HermaLikePiece:
    def __init__(self, file_name, origin=(60, 0, 0), temporal_rule=lambda:1, tempo=60):
        self.temporal_rule = temporal_rule
        self.sections = []
        self.events_list = []
        self.midi_stream = MIDIFile(2)
        self.file_name = file_name
        self.origin = origin
        self.tempo=tempo

        self.session = Session(self.tempo)

    def add_section(self, section):
        self.sections.append(section)

    def set_sections(self, sections):
        self.sections = sections

    def run_composer(self, sequential=False):

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
    
    # Supõe que um evento sonoro já é gerado pela seção com h, g, u corretos 
    # E um offset correto dentro da seção
    def generate_vectors(self, seq):
        
        offset = 0
        for section in self.sections:
            if len(section.event_set)!=0:
                text = m21.expressions.TextExpression('Transição')

                section.generate_section()
                section.offset = offset if seq else section.offset
                events = map(lambda e: SonicEvent(e.h, e.g, e.u, offset=e.offset+section.offset, track=e.track, channel=e.channel), section.events_list)
                self.events_list += events
                offset += section.duration


    #DEPRECATED METHODS
    def midi_to_piano_roll(self):
        p = ppr.read(self.file_name+".mid")
        p.plot()

    def dict_insertion(self, dict, key, value):
        if key not in dict:
            dict[key] = [value]
        
        else:
            dict[key].append(value)

    def transform_vectors_into_mxl(self):
        '''
            Método para exportar musicxml utilizando o SCAMP
        '''
        piano = self.session.new_part('piano')

        events_list = sorted(self.events_list, key=operator.attrgetter('offset'))

        self.session.start_transcribing()
        self.session.fast_forward_in_time(1200)

        next_offset = events_list[0].offset
        cur_offset = 0
        i = 0

        # Actions - 0: stop, 1: start
        note_dict = {next_offset : [(i, 1)]}

        while len(note_dict.keys()) != 0:
            
            for id_or_index, action in note_dict.pop(cur_offset): 

                if action == 1:
                    e = events_list[id_or_index]
                    note = piano.start_note(e.h+self.origin[0], e.g/128)

                    self.dict_insertion(note_dict, e.offset+e.u, (note.note_id, 0))

                    if id_or_index+1 < len(events_list):
                        next_on = events_list[id_or_index+1].offset
                        self.dict_insertion(note_dict, next_on, (id_or_index+1, 1))

                else:
                    piano.end_note(id_or_index)

            if len(note_dict) > 0:
                next_offset = min(note_dict.keys())
                sleep_time = next_offset - cur_offset

                wait(sleep_time)

                cur_offset = next_offset
        
        performance = self.session.stop_transcribing()
        performance.to_score().export_music_xml(self.file_name+".xml")
