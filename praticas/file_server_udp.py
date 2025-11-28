import socket, os

host = ''
port = 60000

udp_socket = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
udp_socket.bind((host,port))

while True:
    
    nome_arquivo , src = udp_socket.recvfrom(10)
    print(f'recebi isso:{nome_arquivo.decode('utf-8')} desse ip e porta {src}')
    
    try:
        #abre arquivo
        f  = open(nome_arquivo.decode('utf-8'),'rb')
        tamanho = os.path.getsize(nome_arquivo.decode('utf-8'))
        
        #byte de aviso
        udp_socket.sendto((5).to_bytes(1,'big') , src)
        print(f'enviei isso {(5).to_bytes(1,'big')} por essa porta e ip {src[0],port}')
        
        #tamanho do arquivo
        udp_socket.sendto(tamanho.to_bytes(4 ,'big'), src)
        print(f'enviei isso {int.from_bytes(tamanho.to_bytes(4,'big'))} por essa porta e ip {src[0],port}')
        
        #lendo e enviando o arquivo
        if 4096 >= tamanho: 
            arquivo = f.read(tamanho)
            udp_socket.sendto(arquivo , src)
            print(f'enviei isso {arquivo} por essa porta e ip {src[0],port}')
            
        else:
            while tamanho > 0:
                if tamanho > 4096:
                    pacote = 4096
                    arquivo = f.read(pacote)
                    udp_socket.sendto(arquivo , src)
                    tamanho -= pacote
                else:
                    arquivo = f.read(tamanho)
                    udp_socket.sendto(arquivo , src)
                    tamanho = 0
                print(f'enviei isso {arquivo} por essa porta e ip {src[0],port}')
        
        f.close()
    except FileNotFoundError:
        udp_socket.sendto((0).to_bytes(1,'big') , src)
    
    
    break

print('ola')
udp_socket.close()
