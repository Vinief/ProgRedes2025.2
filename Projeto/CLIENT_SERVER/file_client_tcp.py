import socket,funcoes,os,sys

encerra_prog = True
parametros = sys.argv

if len(parametros) == 3:
    
    host = parametros[1]
    port = parametros[2]
    tcp_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    
    try:
    
        tcp_socket.connect((host, int(port)))
        encerra_prog = False
    
    except socket.gaierror:
        print('não foi possivel resolver o endereço!!!')
    except ValueError:
        print('a porta tem que ser um numero inteiro!!!')
    except:
        print('houve algum erro!!!')
else:
    print('os parametros n foram passados')

while not encerra_prog:
    try:
        option = int(input('digite a opção:'))
        tcp_socket.send(option.to_bytes(1, "big"))
    
        if option == 10:
            nome_arquivo = input('digite o nome do arquivo:')    
            nome_arquivo_encode = nome_arquivo.encode('utf-8')
            nome_tam = len(nome_arquivo).to_bytes(4 , byteorder = 'big')
            
            funcoes.send(tcp_socket, nome_tam, nome_arquivo_encode)
            print('nome do arquivo enviado com sucesso!!!')

            status = int.from_bytes(tcp_socket.recv(1), "big")
            
            if status == 0:
                f = open(f"../STORAGE_CLIENT/{nome_arquivo}" ,'wb')

                dados = funcoes.recv(tcp_socket)
                print('arquivo recebido com sucesso!!!')


                f.write(dados)
                f.close()

                
        elif option == 20:
            status = int.from_bytes(tcp_socket.recv(1), "big")
        
            if status == 0:
                
                dados = funcoes.recv(tcp_socket)
                print('arquivo recebido com sucesso!!!')

                json = dados.decode('utf-8')
                funcoes.le_json(json)

            else:
                print('houve algum erro')

        elif option == 30:
            enviou_tudo = False
            while not enviou_tudo:
                try:
                    nome_arquivo = input('digite o nome do arquivo que voce deseja upar:')
                    f = open(f'../STORAGE_CLIENT/{nome_arquivo}', 'rb')
                    nome_arquivo_encode = nome_arquivo.encode('utf-8')
                    nome_tam = len(nome_arquivo).to_bytes(4, "big")

                    funcoes.send(tcp_socket, nome_tam, nome_arquivo_encode)
                    print('nome do arquivo enviado com sucesso')

                    status = int.from_bytes(tcp_socket.recv(1), "big")

                    if status == 0:
                        
                        tamanho = os.path.getsize(f'../STORAGE_CLIENT/{nome_arquivo}').to_bytes(4, "big")
                        dado = f.read()

                        funcoes.send(tcp_socket, tamanho, dado)
                        print('arquivo enviado com sucesso!!!')
                        f.close()

                        enviou_tudo = True

                except FileNotFoundError:
                    print('digite o nome de um arquivo que existe!!!')

        elif option == 60:
            print('programa encerrado com sucesso!!!')
            encerra_prog = True 
        else:
            print('essa opcao nao existe!!!')
        
        
    except ValueError:
        print('digite um numero inteiro!!!')
    except:
        print('houve algum erro')


tcp_socket.close()
