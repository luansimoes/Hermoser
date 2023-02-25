import PySimpleGUI as sg
from tkinter import Tk, font

class HermaInterface:
    def __init__(self):
        sg.theme('DarkTanBlue')

        self.aux_layouts = {
            'main': [
                [sg.Push(), sg.Text("Choose your generation method"), sg.Push()],
                [sg.Text('', size=(0,1))],
                [sg.Push(), sg.Button('Xenakis'), sg.Button('Set-Oriented'), sg.Push()],
            ],

            'generation': [
                [sg.Text('Filename', size=(10,0)), sg.Input(size=(25,0), key='filename', do_not_clear=False)],
                [sg.Text('Size', size=(10,0))],
                [sg.Push(), sg.Radio('12', 'type', key='octave'), sg.Radio('24', 'type', key='two_octave'), sg.Radio('88', 'type', key='88'), sg.Push()],
                [sg.pin(sg.Text('Interval Constraint', size=(15,0), key='const_text', visible=False)), sg.pin(sg.Input(size=(20,0), key='constraint', visible=False, do_not_clear=False))],
                [sg.Text('', size=(0, 1))],
                [sg.Push(), sg.Button('Generate'), sg.Push()],
            ]
        }


        self.layout = [
                [sg.Frame('', 
                    [
                        [sg.VPush()],
                        [sg.Column(self.aux_layouts['main'], key='-MAIN-'), 
                            sg.Column(self.aux_layouts['generation'], key='-GEN-', visible=False)],
                        [sg.VPush()]
                    ], size=(400, 200), border_width=0, element_justification='c')
                ],
                    [sg.Push(), sg.Button('Generate', visible=False), sg.Push()],
                    [sg.Text('', size=(0, 2))],
                    [sg.Push(), sg.Push(), sg.Button('Exit')],
                ]

        self.window = sg.Window("Hermoser", self.layout, font='System')
        self._status = '-MAIN-M'
    
    @property
    def status(self):
        return self._status
    
    def set_status(self, value):
        self.window[self._status[:-1]].update( visible = False )
        self.window[value[:-1]].update( visible = True)
        self._status = value

        if value[-1] == 'S':
            self.window['const_text'].update( visible = True)
            self.window['constraint'].update( visible = True)
        else:
            self.window['const_text'].update( visible = False)
            self.window['constraint'].update( visible = False)
            
    
    def enable_buttons(self):
        self.window['Generate'].update(disabled=False)
        self.window['Exit'].update(disabled=False)
        self.window.refresh()
    
    def disable_buttons(self):
        self.window['Generate'].update(disabled=True)
        self.window['Exit'].update(disabled=True)
        self.window.refresh()
        

    def run(self):
        event, values = self.window.Read()
        return event, values

    def close(self):
        self.window.close()


'''
    Nome do Arquivo: input_texto
    Tamanho: *Oitava    *2 oitavas  *88 teclas
    Método: *Xenakis    *Orientado a Conjuntos
    Botão_Enviar
    
'''