import os
import PySimpleGUI as sg
from threading import Thread

def Tela_Principal():
    sg.theme('Black')
    layout=[
        [sg.Button('APAGAR',key='APAGAR')],
        [sg.Text('Arquivo:'),sg.Text('',key='arquivo')],
        [sg.Text('Progresso:'),sg.Text('',key='arquivo_qtd1'),sg.Text(' '),sg.Text('',key='arquivo_qtd2')],
    ]
    return sg.Window('Apagador de exceptions 1.0.0',layout=layout,finalize=True,font='Verdana',text_justification='c')  

def apagar_exceptions():
    arquivos = os.listdir('C:\\Program Files (x86)\\Valltech\\Serviço API CAP\\')
    pos = 0
    pos1 = 0
    lista_de_arquivos_para_excluir = []

    for x in arquivos:
        arquivo, extensao = os.path.splitext(x)
        if extensao == '.log':
            pos1 += 1
            lista_de_arquivos_para_excluir.append(x)

    window['arquivo_qtd2'].update(pos1)

    for x in lista_de_arquivos_para_excluir:
        try:
            os.remove(f'C:\\Program Files (x86)\\Valltech\\Serviço API CAP\\{x}')
        except:
            pass
        else:
            pos += 1
            window['arquivo'].update(x)   
            window['arquivo_qtd1'].update(pos) 


janela = Tela_Principal()
while True:
    window,event,values = sg.read_all_windows()
    if event == 'APAGAR':
        Thread(target=apagar_exceptions).start()

    elif event == sg.WIN_CLOSED:
        break     
