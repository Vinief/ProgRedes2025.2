import socket, os, funcoes, sys, hashlib, threading

HOST = ''
parametros = sys.argv
PORT = ''
RAIZ = '../STORAGE_SERVER/'
TIMEOUT = 300
ENDIANESS = 'big'

if len(parametros) == 2:
    try:
        PORT = int(parametros[1])
        tcp_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        tcp_socket.bind((HOST,PORT))
        tcp_socket.listen(1)
        encerrar_prog = False
    except ValueError:
        print('a porta precisa ser um numero inteiro!!!')
else:
    print('os parametros nao foram passados')

###################################################################################################################################
def server (con,src):
    encerrar_prog = False
    while not encerrar_prog:
        print(f'esperando resposta do cliente...')
        try:
            option = int.from_bytes(con.recv(1), 'big')
            print(f'recebi a opção selecionada:{option} desse host e porta:{src}')
        except ValueError:
            print("usuario n enviou numero inteiro")
            status = (0).to_bytes(1,ENDIANESS)
            con.send(status)
        except:
            print("houve algum error")
            status = (0).to_bytes(1,ENDIANESS)
            con.send(status)
    ###################################################################################################################################
        if option == 10:#opção de download
        
            try:
                #recebe nome e tam do nome 
                nome_arquivo = (funcoes.recv(con)).decode('utf-8')
                print('nome do arquivo recebido com sucesso!!!')
                
                #abre arquivo e pega o tamanho
                if funcoes.valida_caminho(RAIZ,nome_arquivo):
                    f  = open(f'{RAIZ}{nome_arquivo}','rb')
                    tamanho = (os.path.getsize(f'{RAIZ}{nome_arquivo}')).to_bytes(4, ENDIANESS)
                    
                    #retorna se existe
                    status = (0).to_bytes(1, ENDIANESS)
                    con.send(status)
                    
                    dado = f.read()
                    funcoes.send(con, tamanho, dado)
                    print('arquivo enviado com sucesso!!!')
                    
                    f.close()
                    con.close()
                    encerrar_prog = True
                else:
                    status = (1).to_bytes(1, ENDIANESS)
                    con.send(status)
                    print('caminho fora do escopo!!!')
                    con.close()
                    encerrar_prog = True
            except FileNotFoundError:
                status = (1).to_bytes(1, ENDIANESS)
                con.send(status)
                print('arquivo n exite!!!')
                con.close()
                encerrar_prog = True
    ###################################################################################################################################
        elif option == 20:#opção de listagem
            
            status = (0).to_bytes(1, ENDIANESS)
            con.send(status)

            info = funcoes.faz_jason()
            tam_json, dado = (info[0]).to_bytes(4, ENDIANESS), info[1].encode('utf-8')


            funcoes.send(con, tam_json, dado)
            print('arquivo enviado com sucesso!!!')
            con.close()
            encerrar_prog = True
    ###################################################################################################################################
        elif option == 30:#opção de upload
            
            nome_arquivo = (funcoes.recv(con)).decode('utf-8')
            print('nome recebido com sucesso!!!')
            f = open(f'{RAIZ}{nome_arquivo}', 'wb')
            
            status = (0).to_bytes(1, ENDIANESS)     
            con.send(status)

            dado = funcoes.recv(con)
            print('arquivo recebido com sucesso!!!')
            
            f.write(dado)
            f.close()
            
            con.close()
            encerrar_prog = True
            
    ###################################################################################################################################
        elif option == 40:
            nome_arquivo = (funcoes.recv(con)).decode('utf-8')
            try:
                if funcoes.valida_caminho(RAIZ,nome_arquivo):
                    f = open(f'{RAIZ}{nome_arquivo}', 'rb')
                    inicia = int.from_bytes(con.recv(4), ENDIANESS)
                    
                    hash_recv_MD5 = int.from_bytes(con.recv(16))
                    hash_MD5 = int(hashlib.md5(f.read(inicia)).hexdigest(), 16)

                    print(hash_MD5, hash_recv_MD5)

                    tamanho = (os.path.getsize(f'{RAIZ}{nome_arquivo}') - inicia)
                    tamanho_bytes = tamanho.to_bytes(4, ENDIANESS)
                    
                    f.seek(inicia)
                    dado = f.read(tamanho)
                    print(dado)
                    
                    status = (0).to_bytes(1, ENDIANESS)
                    con.send(status)
                    if hash_MD5 == hash_recv_MD5:
                        status = (0).to_bytes(1, ENDIANESS)
                        con.send(status)
                        funcoes.send(con, tamanho_bytes, dado)
                        con.close()
                        encerrar_prog = True

                    else:
                        status = (20).to_bytes(1, ENDIANESS)
                        con.send(status)
                        print('o hash dos arquivos nao bate!!!')
                        con.close()
                        encerrar_prog = True
                
                else:
                    status = (1).to_bytes(1, ENDIANESS)
                    con.send(status)
                    print('caminho fora do escopo!!!')
                    con.close()
                    encerrar_prog = True
            
            except ValueError:
                status = (1).to_bytes(1, ENDIANESS)
                con.send(status)
                print('o byte onde o arquivo inicia deve ser um inteiro!!!')
                con.close()
                encerrar_prog = True

            except FileNotFoundError:
                status = (0).to_bytes(1, ENDIANESS)
                con.send(status)
                status = (10).to_bytes(1, ENDIANESS)
                con.send(status)
                print('arquivo n existe!!!')
                con.close()
                encerrar_prog = True
#######################################################################################################################################
        elif option == 60:
            print('programa encerrado com sucesso!!!')
            encerrar_prog = True
        
        else:
            status = (0).to_bytes(1, ENDIANESS)
            con.send(status)
            con.close()
            encerrar_prog = True
            print('essa opcao nao existe!!!')
#######################################################################################################################################

while True:
    con, src = tcp_socket.accept()
    print(f'conexão aceita de:{src}')
    threading.Thread(target=server, args=(con,src)).start()

