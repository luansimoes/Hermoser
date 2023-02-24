import PySimpleGUI as sg
from tkinter import Tk, font
#from kivymd.app import MDApp
#from kivymd.uix.screen import Screen
#from kivymd.uix.label import MDLabel
#from kivymd.uix.button import MDRoundFlatButton

class HermaInterface:
    def __init__(self):
        sg.theme('DarkTanBlue')

        self.aux_layouts = {
            'main': [
                [sg.Push(), sg.Text("Choose your generation method"), sg.Push()],
                [sg.Text('', size=(0,1))],
                [sg.Push(), sg.Button('Xenakis'), sg.Button('Set-Oriented'), sg.Push()],
            ],

            'xenakis': [
                [sg.Text('Filename', size=(10,0)), sg.Input(size=(25,0), key='filename')],
                [sg.Text('Size', size=(10,0))],
                [sg.Push(), sg.Radio('12', 'type', key='octave'), sg.Radio('24', 'type', key='two_octave'), sg.Radio('88', 'type', key='88'), sg.Push()],
                [sg.Text('', size=(0, 1))],
                [sg.Push(), sg.Button('Generate'), sg.Push()],
            ],

            'set-oriented': [
                [sg.Text('Filename', size=(10,1)), sg.Input(size=(25,0), key='filename')],
                [sg.Text('Size', size=(10,0))],
                [sg.Push(), sg.Radio('12', 'type', key='octave'), sg.Radio('24', 'type', key='two_octave'), sg.Radio('88', 'type', key='88'), sg.Push()],
                [sg.Text('Interval Constraint', size=(15,0)), sg.Input(size=(20,0), key='constraint')],
                [sg.Text('', size=(0, 1))],
                [sg.Push(), sg.Button('Generate'), sg.Push()],
            ]
        }


        self.layout = [
                [sg.Frame('', 
                    [
                        [sg.VPush()],
                        [sg.Column(self.aux_layouts['main'], key='-MAIN-'), 
                            sg.Column(self.aux_layouts['xenakis'], key='-XEN-', visible=False), 
                            sg.Column(self.aux_layouts['set-oriented'], key='-SO-', visible=False)],
                        [sg.VPush()]
                    ], size=(400, 200), border_width=0, element_justification='c')
                ],
                    
                    [sg.Text('', size=(0, 2))],
                    [sg.Push(), sg.Push(), sg.Button('Exit')],
                ]

        self.window = sg.Window("Hermoser", self.layout, font='System')
        self._status = '-MAIN-'
    
    @property
    def status(self):
        return self._status
    
    def set_status(self, value):
        self.window[self._status].update( visible = False )
        self.window[value].update( visible = True)
        self._status = value
        

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