#IMPORTANDO BIBLIOTECAS
import os
import sys
import PySimpleGUI as sg
import time
from threading import Thread

#CÓDIGO DA INTERFACE GRÁFICA
def Tela_Principal():
    sg.theme('Reddit')
    layout=[
        [sg.Button('APAGAR',key='APAGAR',border_width=3),sg.Button('AUTO',key='AUTO',border_width=3),sg.Button('LIMPAR',key='LIMPAR',border_width=3),sg.Button('LISTAR',key='LISTAR',border_width=3)],
        [sg.FolderBrowse('BUSCAR'),sg.Input('',key='diretorio',border_width=1)],
        [sg.Text('Extensão: '),sg.Input(key='ext',size=(4,4),border_width=1)],
        [sg.Text('Arquivo:'),sg.Text('',key='arquivo')],
        [sg.Text('Arquivos apagados: '),sg.Text('',key='arquivo_qtd1')],
        [sg.Text('Total de arquivos na pasta: '),sg.Text('',key='arquivo_qtd2')],
    ]
    return sg.Window('Apagador de exceptions 2.0',layout=layout,finalize=True,font='Verdana',text_justification='c')


def Tela_AUTO():
    sg.theme('Reddit')
    layout=[
        [sg.Text('H:'),sg.Combo(['00','08','12','16','20','22','02','03'],size=(3,3),readonly=True,default_value='00',key='hour'),sg.Text('M:'),sg.Combo(['00','10','20','30','40','50'],size=(3,3),readonly=True,default_value='00',key='minute')],
        [sg.Button('INICIAR',key='INICIAR',border_width=3)],
        [sg.Text('',key='info',background_color='yellow',text_color='red',visible=False)]
    ]
    return sg.Window('Apagador de exceptions 2.0',layout=layout,finalize=True,font='Verdana',text_justification='c')


def get_diretorio():
    diretorio = values['diretorio']
    return(diretorio)

    
            
#ABRINDO JANELA
janela,janela1 = Tela_Principal(),''
while True:
    window,event,values = sg.read_all_windows()

    #APAGA ARQUIVOS E PASTAS!
    if event == 'APAGAR':
        window['APAGAR'].update(disabled=True)
        window['LIMPAR'].update(disabled=True)
        window['AUTO'].update(disabled=True)
        window['LISTAR'].update(disabled=True)
        window['BUSCAR'].update(disabled=True)
        #LISTANDO TODOS ARQUIVOS DO DIRETÓRIO
        try:
            res = get_diretorio()
            arquivos = os.listdir(res)

        except Exception as erro:
            window['arquivo'].update(erro)        

        else:
            window['arquivo_qtd2'].update(len(arquivos))    
            if len(values['ext']) == 0:
                pos = 0
                for x in arquivos:
                    janela.refresh()
                    pos += 1
                    try:
                        os.remove(f'{res}//{x}')
                        window['arquivo'].update(x)
                        window['arquivo_qtd1'].update(pos)

                    except Exception as erro:
                        window['arquivo'].update(erro)
                        continue        
                           
            else:
                pos = 0
                for x in arquivos:
                    janela.refresh()
                    try:
                        z, extensao = os.path.splitext(x)
                        if extensao == values['ext']:
                            pos += 1
                            os.remove(f'{res}//{x}')
                            window['arquivo'].update(x)
                            window['arquivo_qtd1'].update(pos)
                        
                        
                    except Exception as erro:
                        window['arquivo'].update(erro)
                        continue
                          
        #ATIVANDO BOTÕES NOVAMENTE
        window['APAGAR'].update(disabled=False)
        window['LIMPAR'].update(disabled=False)
        window['AUTO'].update(disabled=False)
        window['LISTAR'].update(disabled=False)
        window['BUSCAR'].update(disabled=False)

    #LIMPAR CAMPOS
    elif event == 'LIMPAR':
        window['arquivo'].update('')
        window['arquivo_qtd1'].update('')
        window['arquivo_qtd2'].update('')
        window['diretorio'].update('')
        window['ext'].update('')

    elif event == 'AUTO':
        janela.close()
        janela1 = Tela_AUTO()
      
    
    elif event == 'LISTAR':
        res = get_diretorio()
        arquivos = os.listdir(res)
        qtd = len(values['ext'])
        pos = 0
        pos1 = 0
        lista = []
        for x in arquivos:
            z, extensao = os.path.splitext(x)
            pos1+=1
            if extensao == values['ext'] and qtd > 0:
                try:
                    os.chdir(f'{res}//{x}//')
                except:
                    pos += 1
                    continue

            if len(values['ext']) == 0:
                try:
                    os.chdir(f'{res}//{x}//')
                except Exception as erro:
                    pos += 1
                    continue 
        try:
            arquivos = os.listdir(res)
        except Exception as erro:
            sg.popup(erro)   
        else:
            for x in arquivos:
                z, extensao = os.path.splitext(x)
                try:
                    os.chdir(f'{res}//{x}')

                except Exception as erro:
                    if extensao == values['ext'] and qtd > 0:
                        lista.append(x)
                        continue
                    elif qtd == 0:
                        lista.append(x)  
                        continue
                    

            sg.popup(f"""Arquivos para apagar encontrados: {pos}
            Itens totais encontrados: {pos1}
            {lista}""")     


    

    elif event == 'INICIAR':
        window['info'].update(visible=True)
        hora_escolhida = values['hour']
        hora_escolhida = str(hora_escolhida)
        minuto_escolhido = values['minute']
        minuto_escolhido = str(minuto_escolhido)
        while True:
            h = time.strftime('%H')
            m = time.strftime('%M')
            s = time.strftime('%S')
            h = str(h)
            m = str(m)
            if hora_escolhida == h and minuto_escolhido == m:
                print('nao sei')
            window['info'].update(f'[{h}:{m}:{s}]Esperando horário...')    
            janela1.refresh()
            time.sleep(10)
            


    #FINALIZA O PROGRAMA        
    elif event == sg.WIN_CLOSED:
        break     
