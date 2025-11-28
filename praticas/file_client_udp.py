import socket

host = '127.0.0.1'
port = 60000

udp_socket = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)

msg_recebida = ''

while True:
    
    arquivo = 'alo.txt'
    
    #envia nome do arquivo
    udp_socket.sendto(arquivo.encode('utf-8') , (host,port))
    print(f'enviei isso {arquivo} por essa porta e ip {port,host}')
    
    #recebe retorno do servidor se o arquivo existe
    retorno , src = udp_socket.recvfrom(1)
    print(f'recebi isso:{retorno.decode} desse ip e porta {src}')
    
    if int.from_bytes(retorno) != 0:
        #recebe o tamanho do arquivo
        tamanho , src = udp_socket.recvfrom(4)
        print(f'recebi isso:{tamanho} desse ip e porta {src}')
        f = open('OLAH','wb')
        if tamanho <= 4096:
        #recebe dados do arquivo e escreve
            dados , src = udp_socket.recvfrom(int.from_bytes(tamanho))
            print(f'recebi isso:{dados} desse ip e porta {src}')
            f.write(dados)
            f.close()
        else:
            while tamanho > 0:
                if tamanho > 4096:
                    pacote = 4096
                    arquivo, src = udp_socket.recvfrom(pacote)
                    f.write(arquivo)
                    tamanho -= pacote
                else:
                    arquivo, src = udp_socket.recvfrom(tamanho)
                    f.write(arquivo)
                    tamanho = 0

                print(f'enviei isso {arquivo} por essa porta e ip {src[0],port}')
    else:
        print('arquivo n existe')
    break
udp_socket.close()

