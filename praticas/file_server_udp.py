import socket, os

host = ''
port = 60000

udp_socket = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
udp_socket.bind((host,port))

msg_recebida = ''
data = b''
a = True
while data.decode('utf-8') != '!q':
     
    data , src = udp_socket.recvfrom(1024)
    
    print('recebendo msg...')
    
    f  = open(data.decode('utf-8'),'rb')
    size = os.path.getsize(data.decode('utf-8'))
    
    udp_socket.sendto(size.to_bytes(size.bit_length(),'big'), (src[0],port))
    
    print(src , data.decode('utf-8'))
    
udp_socket.close()
