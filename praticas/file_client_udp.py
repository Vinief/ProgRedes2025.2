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
        data , src = udp_socket.recvfrom(4)
        print(f'recebi isso:{data} desse ip e porta {src}')
        
        #recebe dados do arquivo e escreve
        data , src = udp_socket.recvfrom(int.from_bytes(data))
        print(f'recebi isso:{data} desse ip e porta {src}')
        f = open('OLAH','wb')
        f.write(data)
        f.close()

    else:
        print('arquivo n existe')
    break
udp_socket.close()


print(data.decode('utf-8'))
