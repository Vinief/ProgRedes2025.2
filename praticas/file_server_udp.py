import socket, os,time

host = ''
port = 20000

udp_socket = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
udp_socket.bind((host,port))
print(f'conectado ao host: {host} e a porta: {port}')

nome_arquivo_decode = ''
while nome_arquivo_decode != '!q':
    print(f'esperando resposta do cliente...')
    #recebe tam do nome
    nome_tam , src = udp_socket.recvfrom(1)
    print(f'recebi isso:{int.from_bytes(nome_tam,byteorder = "big")} desse ip e porta {src}')
    
    #recebe nome
    nome_arquivo , src = udp_socket.recvfrom(int.from_bytes(nome_tam,byteorder = "big"))
    nome_arquivo_decode = nome_arquivo.decode('utf-8')
    print(f'recebi isso:{nome_arquivo_decode} desse ip e porta {src}')
    
    try:
        #abre arquivo e pega o tamanho
        f  = open(nome_arquivo.decode('utf-8'),'rb')
        tamanho = os.path.getsize(nome_arquivo.decode('utf-8'))
        
        #byte de aviso
        existe = (1).to_bytes(1,"big") 
        udp_socket.sendto(existe , src)
        print(f'enviei isso {int.from_bytes(existe, byteorder = "big")} por essa porta e ip {src}')
        
        #tamanho do arquivo
        udp_socket.sendto(tamanho.to_bytes(4 ,"big"), src)
        print(f'enviei isso {int.from_bytes(tamanho.to_bytes(4,"big"),byteorder = "big")} por essa porta e ip {src}')
        
        #lendo e enviando o arquivo
        if 4096 >= tamanho: 
            arquivo = f.read(tamanho)
            udp_socket.sendto(arquivo , src)
            print(f'enviei isso {arquivo} por essa porta e ip {src}')
            
        else:
            pacotes = tamanho//4096
            while tamanho > 0:
                if tamanho > 4096:
                    pacote = 4096
                    arquivo = f.read(pacote)
                    udp_socket.sendto(arquivo , src)
                    if f.tell()%200 == 0:
                        time.sleep(0.1)
                        print(f'voce enviou {f.tell()//4096} pacotes de {pacotes}')
                    tamanho -= pacote
                else:
                    arquivo = f.read(tamanho)
                    udp_socket.sendto(arquivo , src)
                    tamanho = 0
                    print(f.tell())
                    print(f'enviei isso {arquivo} por essa porta e ip {src}')
        
        f.close()
    except FileNotFoundError:
        #caso o arquivo n exista
        if nome_arquivo_decode != '!q':
            existe = (0).to_bytes(1,"big")
            udp_socket.sendto((0).to_bytes(1,"big") , src)
            print(f'enviei isso {existe} por essa porta e ip {src}')
        else:print('programa encerrado!!!')

udp_socket.close()
