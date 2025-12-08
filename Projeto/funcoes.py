import os, time, json

###################################################################################################################################
def envio(con,f,tamanho):
    #envia tam
    con.send(tamanho.to_bytes(4 ,"big"))
    print(f'enviei tamanho do arquivo: {int.from_bytes(tamanho.to_bytes(4,"big"),byteorder = "big")} por essa porta e ip: {con}')
    if 1024 >= tamanho:
        #envia arquivo
        arquivo = f.read(tamanho)
        con.send(arquivo)
        print(f'enviei isso {arquivo} por essa porta e ip: {con}')

    else:
        #envia fragmenado
        pacotes = tamanho//pacote
        while tamanho > 0:
            if tamanho > 1024:
                pacote = 1024
                arquivo = f.read(pacote)
                con.send(arquivo)
                if f.tell()%200 == 0:
                    time.sleep(0.1)
                    print(f'voce enviou {f.tell()//1024} pacotes de {pacotes}')
                tamanho -= pacote
            
            else:
                arquivo = f.read(tamanho)
                con.send(arquivo)
                tamanho = 0
                print(f.tell())
                print(f'enviei isso {arquivo} por essa porta e ip: {con}')

###################################################################################################################################
#tem coisa pra arrumar aqui preste atenção seu miseravel
def name_recv(con):    
    #recebe tam do dado
    tamanho_bytes = con.recv(4)
    tamanho = int.from_bytes(tamanho_bytes, byteorder = "big")
    
    if 1024 >= tamanho:
        #recebe arquivo
        dados += con.recv(tamanho)
        print(f'recebi isso:{dados.decode('utf-8')} desse ip e porta')
        
    else:
        #recebe arquivo fragmentado
        pacotes = tamanho//1024
        while tamanho > 0:
            if tamanho > 1024:
                arquivo += con.recv(1024)
                pacote_recv += 1024
                if pacote_recv%50 == 0:
                    time.sleep(0.1)
                    print(f'voce recebeu {pacote_recv//1024} pacotes de {pacotes}')
               
                tamanho -= 1024
            
            else:
                arquivo += con.recv(tamanho)
                print(f'voce recebeu {pacote_recv//1024} pacotes de {pacotes}')
                tamanho = 0

                print(f'enviei isso {arquivo} por essa porta e ip')

    os.path.getsize(arquivo.decode('utf-8'))
    status = (1).from_bytes(1, "big")
    con.send(status)

    return arquivo.decode('utf-8')
###################################################################################################################################
def faz_jason():
    for a in os.listdir('PROJETO/STORAGE_SERVER'):
        json['nome'] = a
        json['tamanho'] = os.path.getsize(f'PROJETO/STORAGE_SERVER/{a}')
        conteudo += json    
        json = {}

    conteudo = f'{conteudo}'
    listagem = open('PROJETO/STORAGE_SERVER/listagem.json' , 'wb')
    listagem.write(conteudo.encode('utf-8'))
    listagem.close()
    return os.path.getsize(f'PROJETO/STORAGE_SERVER/listagem.json')
###################################################################################################################################
def recv (con,f):        
#recebe tam
    tamanho_bytes = con.recv(4)
    tamanho = int.from_bytes(tamanho_bytes, byteorder = "big")
    
    if 1024 >= tamanho:
        #recebe arquivo
        dados = con.recv(tamanho)
        print(f'recebi isso:{dados.decode('utf-8')} desse ip e porta')
        f.write(dados)
        f.close()
    
    else:
        #recebe arquivo fragmentado
        pacotes = tamanho//1024
        while tamanho > 0:
            if tamanho > 1024:
                pacote = 1024
                dados_arquivo = con.recv(pacote)
                if f.tell()%500 == 0:
                    print(f'voce recebeu {f.tell()//1024} pacotes de {pacotes}')
                f.write(dados_arquivo)
                tamanho -= pacote
            
            else:
                dados_arquivo = con.recv(tamanho)
                f.write(dados_arquivo)
                print(f'voce recebeu {f.tell()//1024} pacotes de {pacotes}')
                tamanho = 0

                print(f'enviei isso {dados_arquivo} por essa porta e ip')

def name_send(con, tamanho, nome_arquivo):
#recebe tam do dado
    con.send(tamanho)
    pacote_send = 0
    if 1024 >= tamanho:
        #recebe arquivo
        con.send(nome_arquivo[pacote_send:pacote_send+1024])
        print(f'recebi isso:{nome_arquivo.decode('utf-8')} desse ip e porta')
        
    else:
        #recebe arquivo fragmentado
        pacotes = tamanho//1024
        while tamanho > 0:
            if tamanho > 1024:
                con.send(nome_arquivo[pacote_send:pacote_send+1024])
                pacote_send += 1024
                if pacote_send%50 == 0:
                    time.sleep(0.1)
                    print(f'voce recebeu {pacote_send//1024} pacotes de {pacotes}')
               
                tamanho -= 1024
            
            else:
                con.send(nome_arquivo[pacote_send:pacote_send+1024])
                pacote_send += 1024
                print(f'voce recebeu {pacote_send//1024} pacotes de {pacotes}')
                tamanho = 0

                print(f'enviei isso {nome_arquivo.decode('utf-8')} por essa porta e ip')

    status = 1
    con.recv(status)

    return int.from_bytes(status, "big")

def le_json(arquivo):
    
    json_formatado = json.loads(arquivo)    
    for a in json_formatado:
        print(a)
        print(f'nome: {list(a.values())[0]} tam: {list(a.values())[1]}')
