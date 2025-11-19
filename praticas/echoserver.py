import socket

host = ''
port = 60000

udp_socket = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
udp_socket.bind((host,port))

msg_recebida = ''
data = b''

while data.decode('utf-8') != '!q':
     
    data , src = udp_socket.recvfrom(1024)
    print('recebendo msg...')
    print(src , data.decode('utf-8'))
    
    udp_socket.sendto(data, (src[0],port))


udp_socket.close()
