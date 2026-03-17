import requests, os, time, json, funcoes_bot, threading, socket
PORT = 45678
ENDIANNESS  = 'big'
CODIFICACAO = 'utf-8'
TOKEN       = '8162411623:AAHdj4XLPjL85zI3gubAg-DTPrWimV93Kdk'
URL         = f'https://api.telegram.org/bot{TOKEN}'
info        = []

def aceita_agente():
    global info
    
    ind = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', PORT))
    sock.listen(1)
    while True:
        con, src = sock.accept()
        info += [{'con' : con}]
        info[ind]['src'] = src
        #threading.Thread(target = top_hcpu, args = (con, ind)).start()
        ind += 1

def recv(con):    
    #recebe tam do dado
    tamanho_bytes = con.recv(4)
    tamanho = int.from_bytes(tamanho_bytes, ENDIANNESS)
    print(tamanho)
    arquivo = b''
    pacote_recv = 0
    
    while tamanho > 0:
        if tamanho > 1024:
            arquivo += con.recv(1024)
            pacote_recv += 1024
            tamanho -= 1024
        
        else:
            arquivo += con.recv(tamanho)
            tamanho = 0

    return arquivo




def agentes(parametro):
    ips = [a['src'][0] for a in info]
    texto = f'estes são todos os ips que estou conectado:\n'
    for a in ips:
        texto += f'ip:{a}\n'
        parametro['text'] = texto
        r = requests.post(f'{URL}/sendMessage', params=parametro)
        r.close()

def procs(servico,parametro):
    try:
        ip        = servico.split(' ')[1]
        ip_existe = False        
        for age_src in info:
            if age_src['src'][0] == ip:
                ip_existe = True
                option = ('G').encode(CODIFICACAO)
                age_con = age_src['con']
                age_con.send(option)
                dado = recv(age_con)
                dado = dado.decode(CODIFICACAO)
                dado = json.loads(dado)
                texto = f'estes são os pids de todos os processos desse ip:{ip}\n'
                primeira = True
                for a in dado:
                    if not primeira:
                        texto = ''
                    texto += f'nome:{a["nome"]} - pid:{a["pid"]}\n'
                    if 4096 >= len(texto) >= 3096 or a == dado[len(dado)]:
                        parametro['text'] = texto
                        r = requests.post(f'{URL}/sendMessage', params=parametro)
                        primeira = False
                break
            else:
                if not ip_existe:
                    ip_existe = False
        if not ip_existe:
            texto = 'não estou conectado a este ip!'
            parametro['text'] = texto
            r = requests.post(f'{URL}/sendMessage', params=parametro)

    except IndexError:
        texto = 'vc não passou um dos parametros'
        parametro['text'] = texto
        r = requests.post(f'{URL}/sendMessage', params=parametro)

def proc(servico,parametro):
    try:
        ip, pid = servico.split(' ')[1], int(servico.split(' ')[2])
        ip_existe = False        
        for age_src in info:
            if age_src['src'][0] == ip:
                ip_existe = True
                option = ('P').encode(CODIFICACAO)
                age_con = age_src['con']
                age_con.send(option)
                age_con.send(pid.to_bytes(4, ENDIANNESS))
                dado = json.loads((recv(age_con)).decode(CODIFICACAO))
                print(dado)
                if dado['ok']:
                    texto = (f'estas são todas as informaçoes desse pid:{pid}\n'+
                                f'nome: {dado["nome"]}\n'+
                                f'caminho: {dado["path"]}\n' +
                                f'memoria consumida: {dado["mem"]}\n'+
                                f'cpu usada: {dado["cpu"]}')
                    
                    parametro['text'] = texto
                    r = requests.post(f'{URL}/sendMessage', params=parametro)
                    break
                else:
                    texto = 'houve algum erro pfv tente novamente!'
                    parametro['text'] = texto
                    r = requests.post(f'{URL}/sendMessage', params=parametro)
                    break
            else:
                if not ip_existe:
                    ip_existe = False
        if not ip_existe:
            texto = 'não estou conectado a este ip!'
            parametro['text'] = texto
            r = requests.post(f'{URL}/sendMessage', params=parametro)
    except ValueError:
        texto = 'pid tem que ser um numero inteiro!'
        parametro['text'] = texto
        r = requests.post(f'{URL}/sendMessage', params=parametro)
    except IndexError:
        texto = 'vc não passou um dos parametros'
        parametro['text'] = texto
        r = requests.post(f'{URL}/sendMessage', params=parametro)

def topcpu(servico,parametro):
    try:
        ip = servico.split(' ')[1]
        ip_existe = False
        print(info, ip)
        for age_src in info:
            if age_src['src'][0] == ip:
                ip_existe = True
                option = ('C').encode(CODIFICACAO)
                age_con = age_src['con']
                age_con.send(option)
                dado = json.loads((recv(age_con).decode(CODIFICACAO)))
                texto = f'estas são os cinco processos mais usados da cpu desse ip:{ip}\n'
        
                for a in dado:
                    texto += f'pid:{a["pid"]} - cpu:{a["perc"]}%\n' 
                
                parametro['text'] = texto
                r = requests.post(f'{URL}/sendMessage', params=parametro)
                break
            else:
                if not ip_existe:
                    ip_existe = False
        
        if not ip_existe:
            texto = 'não estou conectado a este ip!'
            parametro['text'] = texto
            r = requests.post(f'{URL}/sendMessage', params=parametro)
    
    except IndexError:
        texto = 'vc não passou o ip da maquina que deseja saber os processos'
        parametro['text'] = texto
        r = requests.post(f'{URL}/sendMessage', params=parametro)

def topmem(servico,parametro):
    try:
        ip = servico.split(' ')[1]
        ip_existe = False
        for age_src in info:
            if age_src['src'][0] == ip:
                ip_existe = True
                option = ('C').encode(CODIFICACAO)
                age_con = age_src['con']
                age_con.send(option)
                dado = json.loads((recv(age_con)).decode(CODIFICACAO))
                texto = f'estas são os processos mais usados da cpu desse ip:{ip}\n'

                for a in dado:
                    texto += f'pid:{a["pid"]} - men:{a["perc"]}%\n' 
                
                parametro['text'] = texto
                r = requests.post(f'{URL}/sendMessage', params=parametro)
    
            else:
                if not ip_existe:
                    ip_existe = False
        if not ip_existe:
            texto = 'não estou conectado a este ip!'
            parametro['text'] = texto
            r = requests.post(f'{URL}/sendMessage', params=parametro)
    except IndexError:
        texto = 'vc não passou o ip da maquina que deseja saber os processos'
        parametro['text'] = texto
        r = requests.post(f'{URL}/sendMessage', params=parametro)

def histcpu(servico,parametro):
    try:
        ip = servico.split(' ')[1]
        ip_existe = False
        for age_src in info:
            if age_src['src'][0] == ip:
                    cpu_usage = sorted(age_src['perc'], key=lambda x: x[1], reverse=True)[0:5]
                    texto = f'''esses são os processos que mais usaram cpu no ultimo minuto:\n
                            1°:{cpu_usage[0]}%\n
                            2°:{cpu_usage[1]}%\n
                            3°:{cpu_usage[2]}%\n
                            4°:{cpu_usage[3]}%\n
                            5°:{cpu_usage[4]}%'''
                    
                    parametro['text'] = texto
                    r = requests.post(f'{URL}/sendMessage', params=parametro)
                    break
            else:
                if not ip_existe:
                    ip_existe = False
        if not ip_existe:
            texto = 'não estou conectado a este ip!'
            parametro['text'] = texto
            r = requests.post(f'{URL}/sendMessage', params=parametro)

    except IndexError:
        texto = 'vc não passou o ip da maquina que deseja saber os processos'
        parametro['text'] = texto
        r = requests.post(f'{URL}/sendMessage', params=parametro)
    

def hardw(servico,parametro):
    try:
        ip = servico.split(' ')[1]
        ip_existe = False
        for age_src in info:
            if age_src['src'][0] == ip:
                    ip_existe = True
                    age_con = age_src['con']
                    option = ('H').encode(CODIFICACAO)
                    age_con.send(option)
                    dado = json.loads((recv(age_con)).decode(CODIFICACAO))
                    texto = (f'estas são informações sobre o hardware desse ip:{ip}\n'+
                                f'memoria swap:{dado['swap_memory']}\n'+
                                f'porcentagem de ram usada:{dado['virtual_memory']}\n'+
                                f'porcentagem da cpu usada:{dado['cpu_percent']}\n'+
                                f'frequencia atual da cpu:{dado['cpu_freq']}\n'+
                                f'quantidade de processos rodando:{dado['total_process']}')
                    
                    parametro['text'] = texto
                    r = requests.post(f'{URL}/sendMessage', params=parametro)
                    break
            else:
                if not ip_existe:
                    ip_existe = False
        if not ip_existe:
            texto = 'não estou conectado a este ip!'
            parametro['text'] = texto
            r = requests.post(f'{URL}/sendMessage', params=parametro)

    except IndexError:
        texto = 'vc não passou o ip da maquina que deseja saber os processos'
        parametro['text'] = texto
        r = requests.post(f'{URL}/sendMessage', params=parametro)

def eval(servico,parametro):
    
    try:
        ip = servico.split(' ')[1]
        ip_existe = False
        for age_src in info:
            if age_src['src'][0] == ip:
                ip_existe = True
                age_con = age_src['con']
                option = ('H').encode(CODIFICACAO)
                age_con.send(option)
                dado = json.loads((recv(age_con)).decode(CODIFICACAO))
                texto = f'''estas são informações sobre o hardware\n
                            memoria swap:{dado['swap_memory']}\n
                            porcentagem de ram usada:{dado['virtual_memory']}\n
                            porcentagem da cpu usada:{dado['cpu_percent']}\n
                            frequencia atual da cpu:{dado['cpu_freq']}\n
                            quantidade de processos rodando:{dado['total_process']}'''
                
                SERVICES = { "gemini"   : { "model" : "gemini-2.5-flash",  # ou gemini-1.5-pro, etc.
                            "host": "generativelanguage.googleapis.com",
                            "endpoint" : "/v1beta/openai/chat/completions",
                            "token": 'AIzaSyCMUoBP4-A5FyfKm3d-1ByzY_y-DSHOrEQ'}
                }

                headers = {
                "Authorization": "AIzaSyCMUoBP4-A5FyfKm3d-1ByzY_y-DSHOrEQ",
                "Content-Type": "application/json"
                }

                payload =  {   "model" : "gemini-2.5-flash", 
                        "messages"   : [ 
                            {"role": "system", "content": "dê diagnostico sobre as informações de hardware a seguir"},
                            {"role": "user", "content": ""} ],
                        "temperature": 0.7,
                        "max_tokens" : 10000
                }

                req_envio = requests.post("https://"+ 
                                        SERVICES['gemini']["host"]+
                                        SERVICES['gemini']["endpoint"], 
                                        headers=headers, json=payload)
                req_envio.raise_for_status()
                req_envio.json()
                texto = req_envio["choices"][0]["message"]["content"].strip()
                parametro['text'] = texto
                r = requests.post(f'{URL}/sendMessage', params=parametro)
                
                break
            else:
                if not ip_existe:
                    ip_existe = False
        if not ip_existe:
            texto = 'não estou conectado a este ip!'
            parametro['text'] = texto
            r = requests.post(f'{URL}/sendMessage', params=parametro)

    except IndexError:
        texto = 'vc não passou o ip da maquina que deseja saber os processos'
        parametro['text'] = texto
        r = requests.post(f'{URL}/sendMessage', params=parametro)
