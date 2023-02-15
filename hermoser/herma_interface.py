import PySimpleGUI as sg
from tkinter import Tk, font
#from kivymd.app import MDApp
#from kivymd.uix.screen import Screen
#from kivymd.uix.label import MDLabel
#from kivymd.uix.button import MDRoundFlatButton

kv = '''
Screen:

    MDRoundFlatButton:
        text: "Gerar Material"
        pos
'''

'''
class HermoserApp(MDApp):
    def build(self):
        screen = Screen()
        screen.add_widget(MDRoundFlatButton(
            text = "Gerar Material",
            pos_hint = {"center_x": 0.5, "center_y": 0.5},
        ))
        return screen
'''

class HermaInterface:
    def __init__(self):
        sg.theme('DarkTanBlue')

        layout = [
            [sg.Text('Filename', size=(10,0)), sg.Input(size=(25,0), key='filename')], 
            [sg.Text('Size', size=(10,0))], 
            [sg.Push(), sg.Radio('12', 'type', key='octave'), sg.Radio('24', 'type', key='two_octave'), sg.Radio('88', 'type', key='88'), sg.Push()],
            [sg.Text('Method', size=(10,0))], 
            [sg.Push(), sg.Radio('Xenakis', 'method', key='xenakis'), sg.Radio('Set-Oriented', 'method', key='set_oriented'), sg.Push()],
            [sg.Push(), sg.Button('Generate'), sg.Push()],
        ]
        self.window = sg.Window("Hermoser", layout, font='System')
        
    #Fazer isso na main
    def run(self):
        event, values = self.window.Read()
        return event, values



'''
    Nome do Arquivo: input_texto
    Tamanho: *Oitava    *2 oitavas  *88 teclas
    Método: *Xenakis    *Orientado a Conjuntos
    Botão_Enviar
    
'''