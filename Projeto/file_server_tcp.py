import socket, os,time

host = ''
port = 20000

tcp_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
tcp_socket.bind((host,port))
tcp_socket.listen(1)
con , cliente = tcp_socket.accept()
###################################################################################################################################
def fragmentar(con,f,tamanho):
    #tamanho do arquivo
    con.send(tamanho.to_bytes(4 ,"big"))
    print(f'enviei tamanho do arquivo: {int.from_bytes(tamanho.to_bytes(4,"big"),byteorder = "big")} por essa porta e ip: {con}')

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
    print(f'enviei o status do arquivo {int.from_bytes(status, byteorder = "big")} por essa porta e ip: {con}')
    
    #recebe tam do dado
    tam = con.recv(1)
    print(f'recebi o tamanho do dado:{int.from_bytes(tam, byteorder = "big")} desse ip e porta ')

    #recebe os dados
    arquivo = con.recv(int.from_bytes(tam,byteorder = "big"))
    print(f'recebi o dado:{arquivo.decode('utf-8')} desse ip e porta {con} ')

    os.path.getsize(nome_arquivo)

    #byte de aviso
    status = (1).to_bytes(1,"big") 
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
def envio_comum(con,f,tamanho):
    #tamanho do arquivo
    con.send(tamanho.to_bytes(4 ,"big"))
    print(f'enviei tamanho do arquivo: {int.from_bytes(tamanho.to_bytes(4,"big"),byteorder = "big")} por essa porta e ip: {con}')

    arquivo = f.read(tamanho)
    con.send(arquivo)
    print(f'enviei isso {arquivo} por essa porta e ip: {con}') 

print(f'conectado ao host: {host} e a porta: {port}')

name_recv_decode = ''
###################################################################################################################################
while name_recv_decode != '!q':
    print(f'esperando resposta do cliente...')
    
    option = int.from_bytes(con.recv(1), 'big')
    print(f'recebi a opção selecionada:{option} desse host e porta:{con}')
    
    if option == 10:
    
        try:
            #recebe nome e tam do nome 
            nome_arquivo = name_recv(con)
            
            #abre arquivo e pega o tamanho
            f  = open(nome_arquivo,'rb')
            tamanho = os.path.getsize(nome_arquivo)
            
            #lendo e enviando o arquivo
            if 1024 >= tamanho: 
                envio_comum(con, f , tamanho)
        
            else:
                fragmentar(con, f , tamanho)
                
            f.close()
        except FileNotFoundError:
            #caso o arquivo n status
            status = (0).to_bytes(1,"big")
            con.send(status)
            print(f'enviei o status do arquivo:{status} por essa porta e ip: {con}')
    
    if option == 20:
        tam_json = faz_jason()
        if 1024 >= tam_json:
            envio_comum(con,f,tam_json)

        else:
            fragmentar(con,f,tam_json)

        f.close()    
    if option == 30:
        nome_arquivo = name_recv(con)

        
###################################################################################################################################


tcp_socket.close()
