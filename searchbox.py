#!/usr/bin/env python3

import PySimpleGUI as sg


layout = [

    [sg.InputText(), sg.Button('Search')],
    [sg.Output(size=(50,20))]
]

w = sg.Window('', layout)

while True:
    event, values = w.read()
    if event is None:
        break

w.close()
