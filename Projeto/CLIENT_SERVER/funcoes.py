import os, time, json

###################################################################################################################################
#tem coisa pra arrumar aqui preste atenção seu miseravel
def recv(con):    
    #recebe tam do dado
    tamanho_bytes = con.recv(4)
    tamanho = int.from_bytes(tamanho_bytes, byteorder = "big")
    arquivo = b''
    pacote_recv = 0
    if 1024 >= tamanho:
        #recebe arquivo
        arquivo = con.recv(tamanho)
        
    else:
        #recebe arquivo fragmentado
        pacotes = tamanho//1024
        while tamanho > 0:
            if tamanho > 1024:
                arquivo += con.recv(1024)
                pacote_recv += 1024
                if pacote_recv%200 == 0:
                    print(f'voce recebeu {int(((pacote_recv//1024)/pacotes)*100)}%')
               
                tamanho -= 1024
            
            else:
                arquivo += con.recv(tamanho)
                print(f'voce recebeu {pacote_recv//1024} pacotes de {pacotes}')
                tamanho = 0

    return arquivo
###################################################################################################################################
def faz_jason():
    json_unformated = {}
    conteudo = []
    for a in os.listdir('../STORAGE_SERVER'):
        json_unformated['nome'] = a
        json_unformated['tamanho'] = os.path.getsize(f'../STORAGE_SERVER/{a}')
        conteudo += [json_unformated]    
        json_unformated = {}

    conteudo = json.dumps(conteudo)
    return [len(conteudo), conteudo]
###################################################################################################################################
def send(con, tamanho, dados):
#recebe tam do dado
    con.send(tamanho)
    pacote_send = 0
    
    tamanho = int.from_bytes(tamanho, "big")

    if 1024 >= tamanho:
        #recebe arquivo
        con.send(dados)
        
    else:
        #recebe arquivo fragmentado
        pacotes = tamanho//1024
        while tamanho > 0:
            if tamanho > 1024:
                con.send(dados[pacote_send:pacote_send+1024])
                pacote_send += 1024
                if pacote_send%50 == 0:
                    time.sleep(0.1)
                    print(f'voce enviou {int((((pacote_send//1024)/pacotes)*100))}% do pacote')
               
                tamanho -= 1024
            
            else:
                con.send(dados[pacote_send:pacote_send+tamanho])
                pacote_send += tamanho
                print(f'voce enviou {int(((pacote_send//1024)/pacotes)*100)}% do pacote')
                tamanho = 0

def le_json(arquivo):
    json_formatado = json.loads(arquivo)    
    for a in json_formatado:
        print(f'nome: {a['nome']} tamanho: {a['tamanho']}')

#valida caminho
def valida_caminho(raiz, path):
    caminho_real = os.path.realpath(raiz + path)
    raiz = os.path.realpath(raiz)
    
    if (caminho_real).startswith(raiz):
        return True
    else:
        return False 