from hermoser.herma_interface import HermaInterface, sg #HermoserApp
from hermoser.core import *
import random as rd

def check_valid_fields(fields):
    if fields['filename'].isspace() or not fields['filename']:
        return False
    if not(fields['88'] or fields['two_octave'] or fields['octave']):
        return False
    if not(fields['xenakis'] or fields['set_oriented']):
        return False
    
    return True

def configure_so_sections(r, a, b, c, na, nb, nc):
    sections = [
        SetOrientedSection(r),
        SetOrientedSection(a),
        SetOrientedSection(na),
        SetOrientedSection(b),
        SetOrientedSection(nb),
        SetOrientedSection(c),
        SetOrientedSection(nc),

        SetOrientedSection(a*b),
        SetOrientedSection(b*c),
        SetOrientedSection(na*nb + a*b),
        SetOrientedSection(a*b*c),
        SetOrientedSection(na*nb*c),
        SetOrientedSection((a*b+na*nb)*c),
        SetOrientedSection(nb*nc),
        SetOrientedSection(r - (na*nb + a*b)),
        SetOrientedSection(a*nb*nc),
        SetOrientedSection(nc*(r-(na*nb + a*b))),
        SetOrientedSection(na*nc),
        SetOrientedSection(na*b*nc),
        SetOrientedSection(c*(a*b + na*nb)),
        SetOrientedSection(a*b*c + a*nb*nc + na*b*nc + na*nb*c),
    ]
    return sections

# Configurando seções identicas ao planejamento composicional de xenakis
# TODO : Pensar em utilizar distribuição exponencial para escolha dos offsets como fez xenakis
def configure_xen_sections(r, a, b, c, na, nb, nc, tax):
    sections = [
        HermaSection(r, 36.5*tax, [(14*tax,1.73/tax), (23*tax,2.8/tax), (28.5*tax,4.53/tax), (32*tax,7.32/tax), (34.5*tax,11.8/tax), (36*tax,19/tax), (36.5*tax,31/tax)], offset=0, dyn=40),
        HermaSection(a, 46*tax, [(46*tax, 0.8/tax)], offset=36.5*tax, dyn=100),
        HermaSection(a, 16*tax, [(16*tax, 3.3/tax)], offset=45*tax, dyn=20),
        HermaSection(a, 12.5*tax, [(12.5*tax, 5/tax)], offset=70*tax, dyn=20),
        HermaSection(na, 26*tax, [(26*tax, 10/tax)], offset=100*tax, dyn=100),
        HermaSection(b, 14*tax, [(14*tax, 1.76/tax)], offset=126*tax, dyn=80),
        HermaSection(b, 14*tax, [(14*tax, 3.3/tax)], offset=128*tax, dyn=20),
        HermaSection(b, 1*tax, [(1*tax, 5/tax)], offset=134*tax, dyn=20),
        HermaSection(b, 24*tax, [(24*tax, 5/tax)], offset=138*tax, dyn=20),
        HermaSection(b, 19*tax, [(19*tax, 1.76/tax)], offset=150*tax, dyn=80),
        HermaSection(nb, 22*tax, [(22*tax, 10/tax)], offset=182*tax, dyn=100),
        HermaSection(c, 18*tax, [(18*tax, 2.5/tax)], offset=208*tax, dyn=20),
        HermaSection(c, 10*tax, [(10*tax, 5/tax)], offset=212*tax, dyn=100),
        HermaSection(nc, 34*tax, [(34*tax, 9/tax)], offset=216*tax, dyn=100),
        HermaSection(a*b, 6*tax, [(6*tax, 0.8/tax)], offset=256*tax, dyn=20),
        HermaSection(b*c, 4*tax, [(4*tax, 0.8/tax)], offset=270*tax, dyn=80),
        HermaSection(a*b, 4*tax, [(4*tax, 10/tax)], offset=256*tax, dyn=20),
        HermaSection(na*nb + a*b, 12*tax, [(12*tax, 20/tax)], offset=278*tax, dyn=20),
        HermaSection(b*c, 2*tax, [(2*tax, 5/tax)], offset=285*tax, dyn=80),
        HermaSection(a*b*c, 4*tax, [(4*tax, 6/tax)], offset=287*tax, dyn=120),
        HermaSection(na*nb + a*b, 4*tax, [(4*tax, 20/tax)], offset=294*tax, dyn=20),
        HermaSection(na*nb*c, 6*tax, [(6*tax, 6/tax)], offset=296*tax, dyn=120),
        HermaSection((a*b+na*nb)*c, 8*tax, [(8*tax, 12/tax)], offset=298*tax, dyn=100),
        HermaSection(b*c, 2*tax, [(2*tax, 6/tax)], offset=300*tax, dyn=80),
        HermaSection(nb*nc, 8*tax, [(8*tax, 10/tax)], offset=302*tax, dyn=80),
        HermaSection(r - (na*nb + a*b), 12*tax, [(12*tax, 1/tax)], offset=306*tax, dyn=20),
        HermaSection(a*nb*nc, 2*tax, [(2*tax, 3/tax)], offset=313*tax, dyn=120),
        HermaSection(nc*(r-(na*nb + a*b)), 17*tax, [(17*tax, 3/tax)], offset=318*tax, dyn=20),
        HermaSection((a*b+na*nb)*c, 2*tax, [(2*tax, 6/tax)], offset=322*tax, dyn=100),
        HermaSection(a*nb*nc, 2*tax, [(2*tax, 3/tax)], offset=338*tax, dyn=120),
        HermaSection(na*nc, 10*tax, [(10*tax, 10/tax)], offset=340*tax, dyn=80),
        HermaSection(nc*(r-(na*nb + a*b)), 2*tax, [(2*tax, 5/tax)], offset=344*tax, dyn=20),
        HermaSection(a*nb*nc, 2*tax, [(2*tax, 1/tax)], offset=346*tax, dyn=120),
        HermaSection(nc*(r-(na*nb + a*b)), 8*tax, [(8*tax, 1/tax)], offset=350*tax, dyn=20),
        HermaSection((a*b+na*nb)*c, 2*tax, [(2*tax, 10/tax)], offset=354*tax, dyn=100),
        HermaSection(na*nc, 16*tax, [(16*tax, 5/tax)], offset=362*tax, dyn=80),
        HermaSection(a*nb*nc, 2*tax, [(2*tax, 5/tax)], offset=366*tax, dyn=120),
        HermaSection(na*b*nc, 2*tax, [(2*tax, 20/tax)], offset=376*tax, dyn=20),
        HermaSection(nc*(r-(na*nb + a*b)), 12*tax, [(12*tax, 1/tax)], offset=382*tax, dyn=20),
        HermaSection(c*(a*b + na*nb), 2*tax, [(2*tax, 3/tax)], offset=386*tax, dyn=100),
        HermaSection(a*nb*nc, 2*tax, [(2*tax, 1/tax)], offset=390*tax, dyn=120),
        HermaSection(na*b*nc, 2*tax, [(2*tax, 3/tax)], offset=394*tax, dyn=120),
        HermaSection(nc*(r-(na*nb + a*b)), 5*tax, [(5*tax, 6/tax)], offset=398*tax, dyn=100),
        HermaSection(a*b*c + a*nb*nc + na*b*nc + na*nb*c, 11*tax, [(11*tax, 20/tax)], offset=414*tax, dyn=120),
    ]

    return sections

def generate_set_oriented(filename, size):

    # Configuração para gerar os pcsets
    octave = list(range(12))
    sizes=[5,5,5]
    durs = [1/8, 1/4, 1/3, 1/2, 2/3, 3/4, 1, 3/2, 2, 4]
    base = 2 #1.265
    d_vector = set(list(range(24)))

    octave_sets = [random_elements(octave, sizes[0])]

    # Sorteando pcsets dentro das restrições
    for i in range(1,3,1):
        actual_set = random_elements(octave, sizes[i])
        while not satisfy_constraints(actual_set, octave_sets, 6):
            actual_set = random_elements(octave, sizes[i])
        octave_sets.append(actual_set)

    # Ampliando os conjuntos para pspace
    pitch_list = octave if size=='octave' else (list(range(24)) if size=='two_octave' else list(range(-39, 49, 1)))
    event_sets = [[], [], []]
    for pitch in pitch_list:
        for i, s in enumerate(octave_sets):
            if pitch%12 in [e.h for e in s]:
                event_sets[i].append(SonicEvent(pitch, 80, 0))

    dur_sets = [set(rd.choices(list(durs), k=7)) for j in range(3)]
    d_vectors = [set(rd.choices(list(range(24)), k=random_size(10, 28))) for i in range(3)]

    #Conjuntos Base
    r = FullSet([SonicEvent(e, 80, 0) for e in pitch_list], set(durs), base=base, dyn_vector=d_vector)
    a = FullSet(event_sets[0], dur_sets[0], base=base, dyn_vector=d_vectors[0])
    b = FullSet(event_sets[1], dur_sets[1], base=base, dyn_vector=d_vectors[1])
    c = FullSet(event_sets[2], dur_sets[2], base=base, dyn_vector=d_vectors[2])

    na = r-a
    nb = r-b
    nc = r-c

    sections = configure_so_sections(r, a, b, c, na, nb, nc)
    piece = HermaLikePiece(f'generated_midi/{filename}', tempo=160)
    piece.set_sections(sections)
    piece.run_composer(sequential=True)

def generate_xenakis(filename, size):
    tempo = 120
    tax = tempo/60

    k = [12] if size=='octave' else ([24] if size=='two_octave' else (-39, 49, 1)) 
    pitch_list = list(range(*k)) 
    sizes = [int(len(pitch_list)/2)-int(len(pitch_list)/12)] * 3

    #event_sets = [random_elements(pitch_list, s) for s in sizes]
    event_sets = random_complete_sets(pitch_list, sizes)
    a, b, c = (EventSet(event_sets[0]), EventSet(event_sets[1]), EventSet(event_sets[2]))
    r = EventSet([SonicEvent(x, 80, 0) for x in pitch_list])

    na = r-a
    nb = r-b
    nc = r-c

    sections = configure_xen_sections(r, a, b, c, na, nb, nc, tax)

    piece = HermaLikePiece(f'generated_midi/{filename}', tempo=tempo)
    piece.set_sections(sections)
    piece.run_composer(sequential=False)



def generate_material(config):
    '''
        Gera o material baseado no método escolhido
    '''
    filename, size, method = config

    if method=='set_oriented':
        generate_set_oriented(filename, size)
    else:
        generate_xenakis(filename, size)


def main_operation(fields):
    '''
        Método que inicializa a geração dos materiais caso os campos estejam corretamente preenchidos
    '''
    valid = check_valid_fields(fields)

    if valid:

        size = 'octave' if fields['octave'] else ('two_octave' if fields['two_octave'] else '88')
        method = 'xenakis' if fields['xenakis'] else 'set_oriented'
        configs = (fields['filename'], size, method)

        generate_material(configs)

    else:
        #TODO: Popup window ou alerta avisando os campos incorretos
        print('NOT VALID')
        pass


if __name__ == '__main__':

    # Inicializa a Interface
    interface = HermaInterface()

    # Exibe a interface e espera por eventos
    event, values = interface.run()
    while event != sg.WINDOW_CLOSED:
        if event == 'Generate':
            main_operation(values)

        event, values = interface.run()


#HermoserApp().run()

#TODO: Interromper botões enquanto gera material, acompanhado de aviso