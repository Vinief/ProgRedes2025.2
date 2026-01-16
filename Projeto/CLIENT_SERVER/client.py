import socket, funcoes, os, sys, hashlib, threading

encerra_prog = False
parametros = sys.argv
RAIZ = "../STORAGE_CLIENT/"
ENDIANESS = 'big'

if len(parametros) == 3:
    try:
        HOST_PORT = (parametros[1],int(parametros[2]))
    except ValueError:
        print('a porta deve se um numero inteiro!!')
        encerra_prog = True

else:
    print('os parametros n foram corretamente')
    encerra_prog = True

def trata_client (tcp_socket, option):
    while not encerra_prog:
        try:
            
            ###################################################################################################################################
            if option == 10:
                nome_arquivo = input('digite o nome do arquivo:')    
                #funcoes.limpar()
                nome_arquivo_encode = nome_arquivo.encode('utf-8')
                nome_tam = len(nome_arquivo).to_bytes(4 , byteorder = 'big')
                
                funcoes.send(tcp_socket, nome_tam, nome_arquivo_encode)
                print('nome do arquivo enviado com sucesso!!!')

                status = int.from_bytes(tcp_socket.recv(1), "big")
                
                if status == 0:
                    f = open(f"{RAIZ}{nome_arquivo}" ,'wb')

                    dados = funcoes.recv(tcp_socket)
                    print('arquivo recebido com sucesso!!!')


                    f.write(dados)
                    f.close()
                    tcp_socket.close()
                
                else:
                    print('houve algum problema!!!')
                    tcp_socket.close()

        ###################################################################################################################################
            elif option == 20:
                #funcoes.limpar()
                status = int.from_bytes(tcp_socket.recv(1), "big")
            
                if status == 0:
                    
                    dados = funcoes.recv(tcp_socket)
                    print('arquivo recebido com sucesso!!!')

                    json = dados.decode('utf-8')
                    funcoes.le_json(json)
                    tcp_socket.close()
                else:
                    print('houve algum erro')
                    tcp_socket.close()

        ###################################################################################################################################
            elif option == 30:
                enviou_tudo = False
                while not enviou_tudo:
                    try:
                        nome_arquivo = input('digite o nome do arquivo que voce deseja upar:')
                        #funcoes.limpar()
                        if funcoes.valida_caminho(RAIZ, nome_arquivo):
                            f = open(f'{RAIZ}{nome_arquivo}', 'rb')
                            nome_arquivo_encode = nome_arquivo.encode('utf-8')
                            nome_tam = len(nome_arquivo).to_bytes(4, "big")

                            funcoes.send(tcp_socket, nome_tam, nome_arquivo_encode)
                            print('nome do arquivo enviado com sucesso')

                            status = int.from_bytes(tcp_socket.recv(1), "big")
                        else:
                            print('camino inacessivel!!!')
                            tcp_socket.close()

                        if status == 0:
                            
                            tamanho = os.path.getsize(f'{RAIZ}{nome_arquivo}').to_bytes(4, "big")
                            dado = f.read()

                            funcoes.send(tcp_socket, tamanho, dado)
                            print('arquivo enviado com sucesso!!!')
                            f.close()
                            tcp_socket.close()

                            enviou_tudo = True
                        else:
                            print('houve algum erro!!!')
                            tcp_socket.close()

                    except FileNotFoundError:
                        print('digite o nome de um arquivo que existe!!!')
        ###################################################################################################################################
            elif option == 40:
                enviou_tudo = False
                nome_arquivo = None
                while not enviou_tudo:
                    try:
                        if nome_arquivo == None:
                            nome_arquivo = input('digite o nome do arquivo:')
                        
                            f = open(f'{RAIZ}{nome_arquivo}', 'rb')

                            nome_arquivo_encode = nome_arquivo.encode('utf-8')
                            nome_tam = len(nome_arquivo).to_bytes(4, 'big')
                            funcoes.send(tcp_socket, nome_tam, nome_arquivo_encode)
                            inicia = int(input('digite de onde voce quer começar o download:'))
                            hash_MD5 = int(hashlib.md5(f.read(inicia)).hexdigest(), 16).to_bytes(16, "big")
        
                            tcp_socket.send(inicia.to_bytes(4, "big"))
                            tcp_socket.send(hash_MD5)
                            
                            f.close()

                            status = int.from_bytes(tcp_socket.recv(1), "big")
                            if status == 0:
                                status = int.from_bytes(tcp_socket.recv(1), "big")
                                
                                if status == 0: 
                                    dado = funcoes.recv(tcp_socket)
                                    f = open(f'{RAIZ}{nome_arquivo}', 'ab')
                                    f.seek(inicia)
                                    f.write(dado)
                                    f.close()
                                    tcp_socket.close()
                                    enviou_tudo = True
                                
                                if status == 10:
                                    print('houve alugum erro')
                                    tcp_socket.close()
                                    enviou_tudo = True
                                
                                if status == 20:
                                    print('o hash não bate!!!')
                                    tcp_socket.close()
                                    enviou_tudo = True
                            
                            else:
                                print('houve algum erro')
                                tcp_socket.close()
                                enviou_tudo = True
                        else:
                            inicia = int(input('digite de onde voce quer começar o download:'))
                            hash_MD5 = (hashlib.md5(f.read(inicia)).hexdigest()).encode('utf-8')

                            tcp_socket.send(inicia)
                            tcp_socket.send(hash_MD5)
                            
                            f.close()

                            funcoes.recv(tcp_socket)
                            dado = funcoes.recv(tcp_socket)
                            f = open(f'{RAIZ}{nome_arquivo}', 'ab')
                            f.seek(inicia)
                            f.write(dado)
                            f.close()
                            
                            tcp_socket.close()
                            enviou_tudo = True

                    
                    except ValueError:
                        print('o onde inicia o donwload deve ser um inteiro!!!')
                    except FileNotFoundError:
                        nome_arquivo = None
                        print('o digite o nome de um arquivo que existe!!!')


            elif option == 60:
                print('programa encerrado com sucesso!!!')
                tcp_socket.close()
                encerra_prog = True 
            else:
                tcp_socket.close()
                print('essa opcao nao existe!!!')
            
        except ValueError:
            tcp_socket.close()
            print('digite um numero inteiro!!!')
        except socket.timeout:
            tcp_socket.close()
            print('a conexao foi encerrada pela inatividade!!!')

while True:
    option = int(input('10 baixa arquivos\n' \
        '20 lista de arquivo\n' \
        '30 upload de arquivos\n' \
        '40 baixa parte de um arquivo\n' \
        '50 baixa por prefixo ou sufixo\n' \
        '60 encerrar programa\n' \
        'a conexão sera encerrada se ' \
        'digite a opção:'))

    option_byte = option.to_bytes(1, ENDIANESS)
    try:
        tcp_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        tcp_socket.settimeout(15)
        tcp_socket.connect(HOST_PORT)
        tcp_socket.send(option_byte)

        threading.Thread(target=trata_client, args=(tcp_socket, option))


    except socket.gaierror:
        print('não foi possivel resolver o endereço!!!')
    
    except ValueError:
        print('a porta tem que ser um numero inteiro!!!')