import socket, time
HOST = '127.0.0.1'
PORT = 20000

tcp_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

tcp_socket.settimeout(5)

tcp_socket.connect((HOST, PORT))
a = 0

while True:
    a += 1
    if a%2000000 == 0:
        print(a)
    if a == 260000000:
        break

print('oie')
tcp_socket.close()
