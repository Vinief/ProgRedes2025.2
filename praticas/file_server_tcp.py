import socket, os,time

host = ''
port = 20000

tcp_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
tcp_socket.bind((host,port))
tcp_socket.listen(1)
con , cliente = tcp_socket.accept()

print(f'conectado ao host: {host} e a porta: {port}')

nome_arquivo_decode = ''
while nome_arquivo_decode != '!q':
    print(f'esperando resposta do cliente...')
    #recebe tam do nome
    nome_tam = con.recv(1)
    print(f'recebi isso:{int.from_bytes(nome_tam,byteorder = "big")} desse ip e porta ')
    
    #recebe nome
    nome_arquivo = con.recv(int.from_bytes(nome_tam,byteorder = "big"))
    nome_arquivo_decode = nome_arquivo.decode('utf-8')
    print(f'recebi isso:{nome_arquivo_decode} desse ip e porta ')
    
    try:
        #abre arquivo e pega o tamanho
        f  = open(nome_arquivo.decode('utf-8'),'rb')
        tamanho = os.path.getsize(nome_arquivo.decode('utf-8'))
        
        #byte de aviso
        existe = (1).to_bytes(1,"big") 
        con.send(existe)
        print(f'enviei isso {int.from_bytes(existe, byteorder = "big")} por essa porta e ip ')
        
        #tamanho do arquivo
        con.send(tamanho.to_bytes(4 ,"big"))
        print(f'enviei isso {int.from_bytes(tamanho.to_bytes(4,"big"),byteorder = "big")} por essa porta e ip ')
        
        #lendo e enviando o arquivo
        if 4096 >= tamanho: 
            arquivo = f.read(tamanho)
            con.send(arquivo)
            print(f'enviei isso {arquivo} por essa porta e ip ')
            
        else:
            pacotes = tamanho//4096
            while tamanho > 0:
                if tamanho > 4096:
                    pacote = 4096
                    arquivo = f.read(pacote)
                    con.send(arquivo)
                    if f.tell()%200 == 0:
                        time.sleep(0.1)
                        print(f'voce enviou {f.tell()//4096} pacotes de {pacotes}')
                    tamanho -= pacote
                else:
                    arquivo = f.read(tamanho)
                    con.send(arquivo)
                    tamanho = 0
                    print(f.tell())
                    print(f'enviei isso {arquivo} por essa porta e ip ')
        
        f.close()
    except FileNotFoundError:
        #caso o arquivo n exista
        if nome_arquivo_decode != '!q':
            existe = (0).to_bytes(1,"big")
            con.send((0).to_bytes(1,"big"))
            print(f'enviei isso {existe} por essa porta e ip ')
        else:print('programa encerrado!!!')

tcp_socket.close()
