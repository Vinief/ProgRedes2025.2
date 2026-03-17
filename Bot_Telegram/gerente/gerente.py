import requests, time, json, funcoes_bot, threading, socket, funcoes_bot

ENDIANNESS  = 'big'
CODIFICACAO = 'utf-8'
TOKEN       = #seu token
URL         = f'https://api.telegram.org/bot{TOKEN}'
PORT        = 45678
sock        = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
update_id = 0
response = {'ok': False, 'result':[]}

threading.Thread(target=funcoes_bot.aceita_agente, args=()).start()

while True:
    parametro = {"offset" : update_id}
    r = requests.get(f'{URL}/getUpdates', params=parametro)
    response = json.loads(r.content)
    
    if response['ok'] and len(response['result']) != 0:
        Message    = response['result'][0]['message']
        servico    = Message['text']
        chat_id    = Message['chat']['id']
        parametro  = {'chat_id':chat_id}
                
        if servico.startswith('/agentes'):
            funcoes_bot.agentes(parametro)
        
        if servico.startswith('/procs'):
            funcoes_bot.procs(servico,parametro)
            
        elif servico.startswith('/proc'):
            funcoes_bot.proc(servico,parametro)
                
        elif servico.startswith('/topcpu'):
            funcoes_bot.topcpu(servico,parametro)

        elif servico.startswith('/topmem'):
            funcoes_bot.topmem(servico,parametro)
            
        elif servico.startswith('/histcpu'):
            funcoes_bot.histcpu(servico,parametro)
            
        elif servico.startswith('/hardw'):
            funcoes_bot.hardw(servico,parametro)
            
        elif servico.startswith('/eval'):
            funcoes_bot.eval(servico,parametro)
        
        if update_id == 0:
            update_id = response['result'][0]['update_id']
        
        else:
            update_id += 1
        
        time.sleep(1)
