import socket, os

host = ''
port = 60000

udp_socket = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
udp_socket.bind((host,port))

msg_recebida = ''
data = b''

while data.decode('utf-8') != '!q':
     
    data , src = udp_socket.recvfrom(1024)
    
    print('recebendo msg...')
    
    f  = open(data.decode('utf-8'),'rb')
    try:
        size = os.path.getsize(data.decode('utf-8'))
             
        udp_socket.sendto((10).to_bytes(1,'big') , (src[0],port))
    
        udp_socket.sendto(size.to_bytes(4 ,'big'), (src[0],port))
        f.read(size)
        f.close()

    except FileNotFoundError:
        udp_socket.sendto((0).to_bytes(1,'big') , (src[0],port))
    
    
    print(src , data.decode('utf-8'))
    
udp_socket.close()
