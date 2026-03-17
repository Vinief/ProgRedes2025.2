import sys, socket, json, psutil, time, threading
PORT = 45678
ENDIANNESS = 'big'
CODIFICACAO = 'utf-8'

if len(sys.argv) == 2:
    try:
        HOST =  sys.argv[1]
        sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        sock.connect((HOST,PORT))
    except socket.gaierror:
        print('n foi possivel se conectar') 

def op_G ():
    pids = psutil.pids()
    dado = []
    for a in pids:
        try:
            dado += [{'pid':a,
                    'nome':psutil.Process(a).name()}]
        except psutil.NoSuchProcess:
            continue
            
    dado = (json.dumps(dado)).encode(CODIFICACAO)
    tam = len(dado).to_bytes(4, ENDIANNESS)
    print(len(dado))
    return tam, dado

def op_P (pid):
    try:
        processo = psutil.Process(pid)
        processo.cpu_percent(interval=None)
        time.sleep(0.1)
    
        dado = json.dumps({"ok" : True, 
            'pid':pid,
            'nome':processo.name(),
            'path':processo.exe(),
            'mem':round(processo.memory_percent(),1),
            'cpu':round(processo.cpu_percent(),1)
            }).encode(CODIFICACAO)
        tam = len(dado).to_bytes(4, ENDIANNESS)
        
        return tam, dado    
    except psutil.NoSuchProcess:
        dado = json.dumps({ "ok" : False }).encode(CODIFICACAO)
        tam  = len(dado).to_bytes(4, ENDIANNESS) 

        return tam, dado


def op_C():
    pids = psutil.pids()
    dado = []
    pid_cpu = {}

    for a in pids:
        try:
            processo = psutil.Process(a)
            processo.cpu_percent(interval=None)
            time.sleep(0.1)
            pid_cpu[f'{a}'] = processo.cpu_percent(interval=None)
        except psutil.NoSuchProcess:
            continue
    
    cpu_g = sorted(pid_cpu.items(), key=lambda x:x [1], reverse=True)[0:5]
    for a in cpu_g:
        dado += [{'pid':a[0],
                  'perc':a[1]}]
        
    dado = json.dumps(dado).encode(CODIFICACAO)    
    tam = len(dado).to_bytes(4, ENDIANNESS)
    return tam, dado

def op_M():
    pids = psutil.pids()
    dado = []
    pid_memory = {}

    for a in pids:
        try:
        
            processo = psutil.Process(a)
            pid_memory[f'{a}'] = round(processo.memory_percent(), 1)
        
        except psutil.NoSuchProcess:
            continue

    memory_g = sorted(pid_memory.items(), key=lambda x: x[1], reverse=True)[0:5]
    
    for a in memory_g:
        dado += [{'pid':a[0],
                  'perc':a[1]}]
    
    dado = json.dumps(dado).encode(CODIFICACAO)    
    tam = len(dado).to_bytes(4, ENDIANNESS)
    print(dado)
    return tam, dado
def op_H():
    dado = {'swap_memory'   : psutil.swap_memory().percent,
            'virtual_memory': psutil.virtual_memory().percent,
            'cpu_percent'   : psutil.cpu_percent(interval=1),
            'cpu_freq'      : psutil.cpu_freq().current,
            'total_process' : len(psutil.pids())}
    
    dado = json.dumps(dado).encode(CODIFICACAO)
    tam = len(dado).to_bytes(4, ENDIANNESS)
    return tam, dado

def send(con, tamanho, dados):
    #envia tam do dado
    con.send(tamanho)
    pacote_send = 0
    tamanho = int.from_bytes(tamanho, ENDIANNESS)
    
    #envia arquivo
    while tamanho > 0:
        if tamanho > 1024:
            con.send(dados[pacote_send:pacote_send+1024])
            tamanho -= 1024
            pacote_send += 1024
        
        else:
            con.send(dados[pacote_send:pacote_send+tamanho])
            tamanho = 0

def envia_dado(option, sock):
    if option == 'G':
        tam, dado = op_G()
        send(sock, tam, dado)
    
    elif option == 'P':
        pid = int.from_bytes(sock.recv(4), ENDIANNESS)
        tam, dado = op_P(pid)
        send(sock, tam, dado)

    elif option == 'C':
        tam, dado = op_C()
        send(sock, tam, dado)
    
    elif option == 'M':
        tam, dado = op_M()
        send(sock, tam, dado)
    
    elif option == 'H':
        tam, dado = op_H()
        send(sock, tam, dado)


while True:

    option = sock.recv(1).decode(CODIFICACAO)
    threading.Thread(target=envia_dado, args=(option, sock)).start()
