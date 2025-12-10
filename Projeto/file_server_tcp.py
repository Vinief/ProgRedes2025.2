import socket, os, funcoes

host = ''
port = 20000

tcp_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
tcp_socket.bind((host,port))
tcp_socket.listen(1)
con , cliente = tcp_socket.accept()

print(f'conectado ao host: {host} e a porta: {port}')

name_recv_decode = ''
###################################################################################################################################
while name_recv_decode != '!q':
    print(f'esperando resposta do cliente...')
    
    option = int.from_bytes(con.recv(1), 'big')
    print(f'recebi a opção selecionada:{option} desse host e porta:{cliente}')
    
    if option == 10:#opção de download
    
        try:
            #recebe nome e tam do nome 
            nome_arquivo = (funcoes.recv(con)).decode('utf-8')
            
            #abre arquivo e pega o tamanho
            print(nome_arquivo)
            f  = open(f'../STORAGE_SERVER/{nome_arquivo}','rb')
            tamanho = (os.path.getsize(f'../STORAGE_SERVER/{nome_arquivo}')).to_bytes(4, "big")
            
            #retorna se existe
            status = (1).to_bytes(1, "big")
            con.send(status)
            
            dado = f.read()
            funcoes.send(con, tamanho, dado)
            print('arquivo enviado com sucesso!!!')
            
            f.close()
        except FileNotFoundError:
            status = (0).to_bytes(1, "big")
            con.send(status)
            print('arquivo n exite!!!')
        
    if option == 20:#opção de listagem
        
        status = (1).to_bytes(1, "big")

        con.send(status)

        tam_json = (funcoes.faz_jason()).to_bytes(4, "big")
        nome = 'listagem.json'
        f = open(f'../STORAGE_SERVER/{nome}', "rb")
        dado = f.read()
        f.close()

        funcoes.send(con, tam_json, dado)
        print('arquivo enviado com sucesso!!!')

    if option == 30:#opção de upload
        try:
            nome_arquivo = (funcoes.recv(con)).decode('utf-8')
            f = open(f'../STORAGE_SERVER/{nome_arquivo}', 'wb')
            status = (1).to_bytes(1, "big")
            
            con.send(status)

            dado = funcoes.recv(con)
            print('arquivo recebido com sucesso!!!')
            
            f.write(dado)
            f.close()
        except FileExistsError:
            #caso o arquivo n exista status
            status = (0).to_bytes(1,"big")
            con.send(status)
            print(f'enviei o status do arquivo:{status} por essa porta e ip: {cliente}')
        
###################################################################################################################################
