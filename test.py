import socket, time
HOST = '127.0.0.1'
PORT = 20000

tcp_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

tcp_socket.connect((HOST, PORT))
tcp_socket.close()
tcp_socket.connect((HOST, PORT))
