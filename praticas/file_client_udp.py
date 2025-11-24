import socket ,os

host = socket.gethostbyname(socket.getfqdn())
port = 60000

para = '10.25.3.43'

udp_socket = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
udp_socket.bind((host,port))

msg_recebida = ''

while msg_recebida != '!q':
    
    mgs = input('digite o nome do arquivo:')
    
    print('enviadando msg...')
    udp_socket.sendto(mgs.encode('utf-8') , (host,port))
    
    print('recebendo msg...')
    data , src = udp_socket.recvfrom(1024)
    
    msg_recebida = data.decode('utf-8')
    print(msg_recebida)

udp_socket.close()


print(data.decode('utf-8'))
