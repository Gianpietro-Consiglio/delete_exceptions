#IMPORTANDO BIBLIOTECAS
import os
import sys
import PySimpleGUI as sg
import time
#CÓDIGO DA TELA PRINCIPAL
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

#CÓDIGO DA TELA AUTO
def Tela_AUTO():
    sg.theme('Reddit')
    layout=[
        [sg.FolderBrowse('BUSCAR'),sg.Input('',key='diretorio',border_width=1)],
        [sg.Text('Extensão: '),sg.Input(key='ext',size=(4,4),border_width=1)],
        [sg.Text('H:'),sg.Combo(['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23'],size=(3,3),readonly=True,default_value='00',key='hour'),sg.Text('M:'),sg.Combo(['00','05','10','15','20','25','30','35','40','45','50','55'],size=(3,3),readonly=True,default_value='00',key='minute')],
        [sg.Button('INICIAR',key='INICIAR',border_width=3),sg.Button('VOLTAR',key='VOLTAR',border_width=3)],
        [sg.Text('',key='info',background_color='yellow',text_color='blue',visible=False)]
    ]
    return sg.Window('Apagador de exceptions 2.0',layout=layout,finalize=True,font='Verdana',text_justification='c')

#FUNÇÃO QUE RETORNA DIRETORIO
def get_diretorio():
    diretorio = values['diretorio']
    return(diretorio)

    
            
#ABRINDO JANELA
janela,janela1 = Tela_Principal(),''
while True:
    window,event,values = sg.read_all_windows()

    #APAGA ARQUIVOS E PASTAS!
    if event == 'APAGAR':
        
        #LISTANDO TODOS ARQUIVOS DO DIRETÓRIO
        try:
            res = get_diretorio()
            arquivos = os.listdir(res)

        except Exception as erro:
           sg.popup(erro) 
           continue       

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
                        sg.popup(erro)
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
                        sg.popup(erro)
                        continue

    #LIMPAR CAMPOS
    elif event == 'LIMPAR':
        window['arquivo'].update('')
        window['arquivo_qtd1'].update('')
        window['arquivo_qtd2'].update('')
        window['diretorio'].update('')
        window['ext'].update('')
    #ABRE OUTRA TELA
    elif event == 'AUTO':
        janela.close()
        janela1 = Tela_AUTO()
      
    #LISTA TODOS OS ARQUIVOS PRESENTES NA PASTA E MOSTRA ARQUIVOS QUE PODEM IR PRO LIXO
    elif event == 'LISTAR':
        res = get_diretorio()
        try:
            os.chdir(res)
        except Exception as erro:
            sg.popup(erro) 
            continue   
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


    
    #CÓDIGO DO BOTÃO INICIAR
    elif event == 'INICIAR':
        window['info'].update(visible=True)
        hora_escolhida = values['hour']
        hora_escolhida = str(hora_escolhida)
        minuto_escolhido = values['minute']
        minuto_escolhido = str(minuto_escolhido)
        while True:
            janela1.refresh()
            h = time.strftime('%H')
            m = time.strftime('%M')
            s = time.strftime('%S')
            h = str(h)
            m = str(m)
            if hora_escolhida == h and minuto_escolhido == m:
                window['info'].update('Excluindo arquivos...')
                diretorio = values['diretorio']
                if len(values['ext']) == 0:
                    try:
                        os.chdir(f'{diretorio}')
                    except Exception as erro:
                        sg.popup(erro)

                    else:
                        arquivos = os.listdir(f'{diretorio}')    
                        for x in arquivos:
                            janela1.refresh()
                            try:
                                os.remove(f'{diretorio}//{x}')    
                                window['info'].update(f'Excluído com sucesso: {x}',background_color='green',text_color='white')
                            except Exception as erro:
                                window['info'].update(f'Falha ao excluir: {x}', background_color='red',text_color='white')
                                continue    
                else:
                    try:
                        os.chdir(f'{diretorio}')
                    except Exception as erro:
                        sg.popup(erro)

                    else:
                        arquivos = os.listdir(f'{diretorio}')    
                        for x in arquivos:
                            janela1.refresh()
                            z, extensao = os.path.splitext(x)
                            if values['ext'] == extensao:
                                try:
                                    os.remove(f'{diretorio}//{x}')  
                                    window['info'].update(f'Excluído com sucesso: {x}',background_color='green',text_color='white')

                                except Exception as erro:
                                    window['info'].update(f'Falha ao excluir: {x}',background_color='red',text_color='white')
                                    continue    


            window['info'].update(f'[{h}:{m}:{s}]Esperando horário...')
            janela1.refresh()
            time.sleep(1)
            
    elif event == 'VOLTAR':
        janela1.close()
        janela = Tela_Principal()

    #FINALIZA O PROGRAMA        
    elif event == sg.WIN_CLOSED:
        break     
