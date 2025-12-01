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
        tamanho , src = udp_socket.recvfrom(4)
        tamanho = int.from_bytes(tamanho)
        print(f'recebi isso:{tamanho} desse ip e porta {src}')
        f = open(input('como vc deseja salvar o arquivo:'),'wb')
        
        if tamanho <= 4096:
        
        #recebe dados do arquivo e escreve
            dados , src = udp_socket.recvfrom(int.from_bytes(tamanho))
            print(f'recebi isso:{dados.decode('utf-8')} desse ip e porta {src}')
            f.write(dados)
        else:
            while tamanho > 0:
                if tamanho > 4096:
                    pacote = 4096
                    dados_arquivo, src = udp_socket.recvfrom(pacote)
                    f.write(dados_arquivo)
                    tamanho -= pacote
                    print(f.tell())
                else:
                    dados_arquivo, src = udp_socket.recvfrom(tamanho)
                    f.write(dados_arquivo)
                    tamanho = 0
                    print(f.tell())
                    print(f'enviei isso {dados_arquivo} por essa porta e ip {src}')
        f.close()
    else:
        if nome_arquivo != '!q':
            print('arquivo n existe')
        else:print('programa encerrado!!!')
            
udp_socket.close()
