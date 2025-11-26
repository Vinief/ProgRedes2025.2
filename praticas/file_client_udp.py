import socket ,os

host = socket.gethostbyname(socket.getfqdn())
port = 60000

udp_socket = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
udp_socket.bind((host,port))

msg_recebida = ''

while msg_recebida != '!q':
    
    arquivo = input('digite o nome do arquivo:')
    
    print('enviadando msg...')
    udp_socket.sendto(arquivo.encode('utf-8') , (host,port))
    
    print('recebendo msg...')
    retorno , src = udp_socket.recvfrom(1)
    
    if int.from_bytes(retorno) != 0:
        
        data , src = udp_socket.recvfrom(4)
        udp_socket.recvfrom(int.from_bytes(data))
        f = open(arquivo,'wb')
        f.write(data)
        f.close()

    else:
        print('arquivo n existe')

udp_socket.close()


print(data.decode('utf-8'))
