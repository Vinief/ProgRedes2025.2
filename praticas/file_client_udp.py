import socket

host = '127.0.0.1'
port = 20000

udp_socket = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)

nome_arquivo = ''

while nome_arquivo != '!q':
    
    nome_arquivo = input('digite o nome do arquivo:')
    nome_arquivo_encode = nome_arquivo.encode('utf-8')
    nome_tam = len(nome_arquivo).to_bytes(1 , byteorder = 'big')

    #envia tam do nome
    udp_socket.sendto(nome_tam , (host,port))
    print(f'enviei isso {nome_tam} por essa porta e ip {port,host}')
    
    #envia nome do arquivo
    udp_socket.sendto(nome_arquivo_encode , (host,port))
    print(f'enviei isso {nome_arquivo} por essa porta e ip {port,host}')
    
    #recebe retorno do servidor se o arquivo existe
    retorno , src = udp_socket.recvfrom(1)
    print(f'recebi isso:{int.from_bytes(retorno)} desse ip e porta {src}')
    
    if int.from_bytes(retorno) != 0:
        
        #recebe o tamanho do arquivo
        tamanho_bytes , src = udp_socket.recvfrom(4)
        tamanho = int.from_bytes(tamanho_bytes, byteorder = 'big')
        print(f'recebi isso:{tamanho} desse ip e porta {src}')
        f = open('eae.jpg','wb')
        
        if tamanho <= 4096:
        
        #recebe dados do arquivo e escreve
            dados , src = udp_socket.recvfrom(tamanho)
            print(f'recebi isso:{dados.decode('utf-8')} desse ip e porta {src}')
            f.write(dados)
            f.close()
        else:
            pacotes = tamanho//4096
            while tamanho > 0:
                if tamanho > 4096:
                    pacote = 4096
                    dados_arquivo, src = udp_socket.recvfrom(pacote)
                    if f.tell()%500 == 0:
                        print(f'voce recebeu {f.tell()//4096} pacotes de {pacotes}')
                    f.write(dados_arquivo)
                    tamanho -= pacote
                else:
                    dados_arquivo, src = udp_socket.recvfrom(tamanho)
                    f.write(dados_arquivo)
                    print(f'voce recebeu {f.tell()//4096} pacotes de {pacotes}')
                    tamanho = 0

                    print(f'enviei isso {dados_arquivo} por essa porta e ip {src[0],port}')
    else:
        if nome_arquivo != '!q':
            print('arquivo n existe')
        else:print('programa encerrado!!!')
            
udp_socket.close()
