import socket, os, funcoes, sys

HOST = ''
parametros = sys.argv
encerrar_prog = True
PORT = ''
RAIZ = '../STORAGE_SERVER/'

if len(parametros) == 2:
    try:
        PORT = int(parametros[1])
        tcp_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        tcp_socket.bind((HOST,PORT))
        tcp_socket.listen(1)
        print(f'conectado ao host: {HOST} e a porta: {PORT}')
        con , cliente = tcp_socket.accept()
        encerrar_prog = False
    except ValueError:
        print('a porta precisa ser um numero inteiro!!!')

###################################################################################################################################
while not encerrar_prog:
    print(f'esperando resposta do cliente...')
    try:
        option = int.from_bytes(con.recv(1), 'big')
        print(f'recebi a opção selecionada:{option} desse host e porta:{cliente}')
    except ValueError:
        print("usuario n enviou numero inteiro")
        status = (0).to_bytes('1',"big")
        con.send(status)
    except:
        print("houve algum error")
        status = (0).to_bytes('1',"big")
        con.send(status)
    
    if option == 10:#opção de download
    
        try:
            #recebe nome e tam do nome 
            nome_arquivo = (funcoes.recv(con)).decode('utf-8')
            print('nome do arquivo recebido com sucesso!!!')
            
            #abre arquivo e pega o tamanho
            if funcoes.valida_caminho(RAIZ,nome_arquivo):
                f  = open(f'{RAIZ}{nome_arquivo}','rb')
                tamanho = (os.path.getsize(f'{RAIZ}{nome_arquivo}')).to_bytes(4, "big")
                
                #retorna se existe
                status = (0).to_bytes(1, "big")
                con.send(status)
                
                dado = f.read()
                funcoes.send(con, tamanho, dado)
                print('arquivo enviado com sucesso!!!')
                
                f.close()
            else:
                status = (1).to_bytes(1, "big")
                con.send(status)
                print('caminho fora do escopo!!!')

        except FileNotFoundError:
            status = (1).to_bytes(1, "big")
            con.send(status)
            print('arquivo n exite!!!')
        
    elif option == 20:#opção de listagem
        
        status = (0).to_bytes(1, "big")
        con.send(status)

        info = funcoes.faz_jason()
        tam_json, dado = (info[0]).to_bytes(4, "big"), info[1].encode('utf-8')


        funcoes.send(con, tam_json, dado)
        print('arquivo enviado com sucesso!!!')

    elif option == 30:#opção de upload
        try:
            nome_arquivo = (funcoes.recv(con)).decode('utf-8')
            print('nome recebido com sucesso!!!')
            f = open(f'{RAIZ}{nome_arquivo}', 'wb')
            
            status = (0).to_bytes(1, "big")     
            con.send(status)

            dado = funcoes.recv(con)
            print('arquivo recebido com sucesso!!!')
            
            f.write(dado)
            f.close()
        except FileExistsError:
            #caso o arquivo n exista status
            status = (1).to_bytes(1,"big")
            con.send(status)
            print(f'enviei o status do arquivo:{status} por essa porta e ip: {cliente}')
    
    elif option == 60:
        print('programa encerrado com sucesso!!!')
        encerrar_prog = True
    
    else:
        print('essa opcao nao existe!!!')
###################################################################################################################################
