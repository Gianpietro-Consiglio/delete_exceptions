#IMPORTANDO BIBLIOTECAS
import os
import sys
import PySimpleGUI as sg
import time
from threading import Thread

#CÓDIGO DA INTERFACE GRÁFICA
def Tela_Principal():
    sg.theme('Black')
    layout=[
        [sg.Button('APAGAR',key='APAGAR'),sg.Button('VERIFICAR',key='VERIFICAR'),sg.Button('AUTO',key='AUTO'),sg.Button('LIMPAR',key='LIMPAR')],
        [sg.Text('Arquivo:'),sg.Text('',key='arquivo',text_color='green')],
        [sg.Text('Exception apagadas: '),sg.Text('',key='arquivo_qtd1',text_color='green')],
        [sg.Text('Total de arquivos: '),sg.Text('',key='arquivo_qtd2')],
    ]
    return sg.Window('Apagador de exceptions 1.0.3',layout=layout,finalize=True,font='Verdana',text_justification='c')

#TRECHO DO CÓDIGO QUE FAZ O PROCEDIMENTO DE APAGAR AS EXCEPTIONS E VERIFICA QUAIS ARQUIVOS SÃO .log
def apagar_exceptions():
    #DESATIVANDO BOTOES PARA QUE DURANTE PROCESSO, USUÁRIO NÃO FIQUE APERTANDO VÁRIAS VEZES OS BOTÕES E ACABE TRAVANDO O PROGRAMA
    window['APAGAR'].update(disabled=True)
    window['LIMPAR'].update(disabled=True)
    window['VERIFICAR'].update(disabled=True)
    window['AUTO'].update(disabled=True)
    #LISTANDO TODOS ARQUIVOS DO DIRETÓRIO
    try:
        arquivos = os.listdir('C:\\Program Files (x86)\\Valltech\\Serviço API CAP\\')
    except Exception as erro:
        sg.popup(erro)
        sys.exit 
    else:
        window['arquivo_qtd2'].update(len(arquivos))            
    
    pos = 0
    #FAZENDO FILTRAGEM DO QUE É .log
    try:
        for x in arquivos:
            arquivo, extensao = os.path.splitext(x)
            if extensao == '.log':
                pos += 1
                os.remove(f'C:\\Program Files (x86)\\Valltech\\Serviço API CAP\\{x}')
                window['arquivo'].update(x)
                window['arquivo_qtd1'].update(pos)
                        
        if pos == 0:
            window['arquivo'].update('Nenhuma exception encontrada!')
            window ['arquivo_qtd1'].update('0')       

    except Exception as erro:
        sg.popup(erro)
        sys.exit()

    else:
        #ATIVANDO BOTÕES NOVAMENTE
        window['APAGAR'].update(disabled=False)
        window['LIMPAR'].update(disabled=False)
        window['VERIFICAR'].update(disabled=False)
        window['AUTO'].update(disabled=False)
        



#ABRINDO JANELA
janela = Tela_Principal()
while True:
    window,event,values = sg.read_all_windows()

    #BOTÃO DE APAGAR EXCEPTIONS. UTILIZEI A BIBLITECA THREAD PARA PODER OBSERVAR EM TEMPO REAL AS EXCEPTIONS SEREM APAGADAS
    if event == 'APAGAR':
        Thread(target=apagar_exceptions).start()

    #BOTÃO VERIFICAR. VERIFICA QUANTAS EXCEPTIONS EXISTEM DENTRO DA PASTA    
    elif event == 'VERIFICAR':
        try:
            arquivos = os.listdir('C:\\Program Files (x86)\\Valltech\\Serviço API CAP\\')
            pos = 0
            lista_de_arquivos_para_excluir = []

            for x in arquivos:
                arquivo, extensao = os.path.splitext(x)
                if extensao == '.log':
                    pos += 1
                    lista_de_arquivos_para_excluir.append(x)
        except Exception as erro:    
            sg.popup(erro)
            sys.exit()    

        else:
            sg.popup(f'Exceptions encontradas: {pos}')        

    #FUNÇÃO DO BOTÃO LIMPAR
    elif event == 'LIMPAR':
        window['arquivo'].update('')
        window['arquivo_qtd1'].update('')
        window['arquivo_qtd2'].update('')

    #FUNÇÃO DO BOTÃO AUTO QUE VERIFICA A CADA 5s o horário atual. Se coincidir com o horário de 23hrs, o mesmo efetua a 
    #função apagar_exeptions
    elif event == 'AUTO':
        hora_planejada = 23
        hora_planejada = str(hora_planejada)
        minuto_planejado = 59
        minuto_planejado = str(minuto_planejado)
        while True:
            if hora_planejada == time.strftime('%H') and minuto_planejado == time.strftime('%M'):
                apagar_exceptions()
            time.sleep(5)  

    #BOTÃO QUE FINALIZA O PROGRAMA        
    elif event == sg.WIN_CLOSED:
        break     
