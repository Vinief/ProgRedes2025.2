import socket

host = '127.0.0.1'
port = 20000

tcp_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
tcp_socket.connect((host, port))

nome_arquivo = ''

while nome_arquivo != '!q':
    
    nome_arquivo = input('digite o nome do arquivo:')
    nome_arquivo_encode = nome_arquivo.encode('utf-8')
    nome_tam = len(nome_arquivo).to_bytes(1 , byteorder = 'big')

    #envia tam do nome
    tcp_socket.send(nome_tam)
    print(f'enviei isso {nome_tam} por essa porta e ip {port,host}')
    
    #envia nome do arquivo
    tcp_socket.send(nome_arquivo_encode)
    print(f'enviei isso {nome_arquivo} por essa porta e ip {port,host}')
    
    #recebe retorno do servidor se o arquivo existe
    retorno = tcp_socket.recv(1)
    print(f'recebi isso:{int.from_bytes(retorno)} desse ip e porta')
    
    if int.from_bytes(retorno) != 0:
        
        #recebe o tamanho do arquivo
        tamanho_bytes = tcp_socket.recv(4)
        tamanho = int.from_bytes(tamanho_bytes, byteorder = 'big')
        print(f'recebi isso:{tamanho} desse ip e porta')
        
        nome = input('digite como vc deseja salvar o arquivo:')
        f = open(nome ,'wb')
        
        if tamanho <= 4096:
        
        #recebe dados do arquivo e escreve
            dados = tcp_socket.recv(tamanho)
            print(f'recebi isso:{dados.decode('utf-8')} desse ip e porta')
            f.write(dados)
            f.close()
        else:
            pacotes = tamanho//4096
            while tamanho > 0:
                if tamanho > 4096:
                    pacote = 4096
                    dados_arquivo = tcp_socket.recv(pacote)
                    if f.tell()%500 == 0:
                        print(f'voce recebeu {f.tell()//4096} pacotes de {pacotes}')
                    f.write(dados_arquivo)
                    tamanho -= pacote
                else:
                    dados_arquivo = tcp_socket.recv(tamanho)
                    f.write(dados_arquivo)
                    print(f'voce recebeu {f.tell()//4096} pacotes de {pacotes}')
                    tamanho = 0

                    print(f'enviei isso {dados_arquivo} por essa porta e ip')
    else:
        if nome_arquivo != '!q':
            print('arquivo n existe')
        else:print('programa encerrado!!!')
            
tcp_socket.close()
