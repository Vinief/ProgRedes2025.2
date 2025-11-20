import funcoes, os ,requests

url = input('digite a sua url:')

pastas = []

def main (r,pastas):
    funcoes.criar_headers(r,pastas)

    if 'text/plain' in r.headers['Content-Type'] :
        pastas += funcoes.criar_plain(r,pastas)
    
    if  'text/html' in r.headers['Content-Type']:
        pastas += funcoes.criar_html(r,pastas)
    
    if 'text/css' in r.headers['Content-Type']:
        pastas += funcoes.criar_css(r,pastas)
    
    if  'text/javascript' in r.headers['Content-Type']:
        pastas += funcoes.criar_javascript(r,pastas)
    
    if 'image/jpeg' in r.headers['Content-Type']:
        pastas += funcoes.criar_jpg(r,pastas)
    
    if  'image/png' in r.headers['Content-Type']:
        pastas += funcoes.criar_png(r,pastas)
    
    if  'image/gif' in r.headers['Content-Type']:
        pastas += funcoes.criar_gif(r,pastas)
    
    if  'audio/mpeg' in r.headers['Content-Type']:
        pastas += funcoes.criar_mpeg(r,pastas)
    
    if  'video/mp4' in r.headers['Content-Type']:
        pastas += funcoes.criar_mp4(r,pastas)
    
    if  'application/json' in r.headers['Content-Type']:
        pastas += funcoes.criar_json(r,pastas)
    
    if  'application/xml' in r.headers['Content-Type']:
        pastas += funcoes.criar_xml(r,pastas)
    
    if  'application/pdf' in r.headers['Content-Type']:
        pastas += funcoes.criar_pdf(r,pastas)
    return pastas
  
r = requests.get(url)

main(r,pastas)




