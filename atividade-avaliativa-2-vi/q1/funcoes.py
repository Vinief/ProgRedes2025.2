import os

def criar_headers(r,pastas):
    if 'headers' not in pastas:
        os.mkdir('/home/dorbado/headers/')
        print('oi')
        f = open(f'/home/dorbado/headers/{([a.replace('.','_') for a in (r.url + '/').split('/') if '.' in a][0]).replace('%','_').replace('#','_').replace('?','_')}.json', 'wb')
        f.write((str(r.headers)).encode('utf-8'))
        f.close
        return 'headers' 
    f = open(f'/home/dorbado/headers/{([a.replace('.','_') for a in (r.url + '/').split('/') if '.' in a][0]).replace('%','_').replace('#','_').replace('?','_')}.json', 'wb')
    f.write(f'{r.content}')
    f.close

def criar_plain(r,pastas):
    if 'content_plain' not in pastas:
        os.mkdir('/home/dorbado/content_plain/')
        f = open(f'/home/dorbado/content_plain/{([a.replace('.','_') for a in (r.url + '/').split('/') if '.' in a][0]).replace('%','_').replace('#','_').replace('?','_')}.plain', 'wb')
        f.write(r.content)
        f.close
        return 'content_plain' 
    f = open(f'/home/dorbado/content_plain/{([a.replace('.','_') for a in (r.url + '/').split('/') if '.' in a][0]).replace('%','_').replace('#','_').replace('?','_')}.plain', 'wb')
    f.write(r.content)
    f.close

def criar_html (r,pastas):
    if 'content_html' not in pastas:
        os.mkdir('/home/dorbado/content_html/')
        f = open(f'/home/dorbado/content_html/{([a.replace('.','_') for a in (r.url + '/').split('/') if '.' in a][0]).replace('%','_').replace('#','_').replace('?','_')}.html', 'wb')
        f.write(r.content)
        f.close
        return'content_html'
    f = open(f'/home/dorbado/content_html/{([a.replace('.','_') for a in (r.url + '/').split('/') if '.' in a][0]).replace('%','_').replace('#','_').replace('?','_')}.html', 'wb')
    f.write(r.content)
    f.close

def criar_css (r,pastas):
    if 'content_css' not in pastas:
        os.mkdir('/home/dorbado/content_css/')
        f = open(f'/home/dorbado/content_css/{([a.replace('.','_') for a in (r.url + '/').split('/') if '.' in a][0]).replace('%','_').replace('#','_').replace('?','_')}.css', 'wb')
        f.write(r.content)
        f.close
        return 'content_css'
    f = open(f'/home/dorbado/content_css/{([a.replace('.','_') for a in (r.url + '/').split('/') if '.' in a][0]).replace('%','_').replace('#','_').replace('?','_')}.css', 'wb')
    f.write(r.content)
    f.close

def criar_javascript(r,pastas):
    if 'content_javascript' not in pastas:
        os.mkdir('/home/dorbado/content_javascript/')
        f = open(f'/home/dorbado/content_javascript/{([a.replace('.','_') for a in (r.url + '/').split('/') if '.' in a][0]).replace('%','_').replace('#','_').replace('?','_')}.javascript', 'wb')
        f.write(r.content)
        f.close
        return 'content_javascript'
    f = open(f'/home/dorbado/content_javascript/{([a.replace('.','_') for a in (r.url + '/').split('/') if '.' in a][0]).replace('%','_').replace('#','_').replace('?','_')}.javascript', 'wb')
    f.write(r.content)
    f.close

def criar_jpg(r,pastas):
    if 'content_jpg' not in pastas:
        os.mkdir('/home/dorbado/content_jpg/')
        f = open(f'/home/dorbado/content_jpg/{((r.url + '/').split('/')[len((r.url + '/').split('/')) - 1]).replace('%','_').replace('#','_').replace('?','_')}.jpg', 'wb')
        f.write(r.content)
        f.close
        return 'content_jpg'
    f = open(f'/home/dorbado/content_jpg/{((r.url + '/').split('/')[len((r.url + '/').split('/')) - 1]).replace('%','_').replace('#','_').replace('?','_')}.jpg', 'wb')
    f.write(r.content)
    f.close

def criar_png(r,pastas):
    if 'content_png' not in pastas:
        os.mkdir('/home/dorbado/content_png/')
        f = open(f'/home/dorbado/content_png/{((r.url + '/').split('/')[len((r.url + '/').split('/')) - 1]).replace('%','_').replace('#','_').replace('?','_')}.png', 'wb')
        f.write(r.content)
        f.close
        return 'content_png'
    f = open(f'/home/dorbado/content_png/{((r.url + '/').split('/')[len((r.url + '/').split('/')) - 1]).replace('%','_').replace('#','_').replace('?','_')}.png', 'wb')
    f.write(r.content)
    f.close

def criar_gif(r,pastas):
    if 'content_gif' not in pastas:
        os.mkdir('/home/dorbado/content_gif/')
        f = open(f'/home/dorbado/content_gif/{((r.url + '/').split('/')[len((r.url + '/').split('/')) - 1]).replace('%','_').replace('#','_').replace('?','_')}.gif', 'wb')
        f.write(r.content)
        f.close
        return 'content_gif'
    f = open(f'/home/dorbado/content_gif/{((r.url + '/').split('/')[len((r.url + '/').split('/')) - 1]).replace('%','_').replace('#','_').replace('?','_')}.gif', 'wb')
    f.write(r.content)
    f.close

def criar_mpeg(r,pastas):
    if 'content_mpeg' not in pastas:
        os.mkdir('/home/dorbado/content_mpeg/')
        f = open(f'/home/dorbado/content_mpeg/{([a.replace('.','_') for a in (r.url + '/').split('/') if '.' in a][0]).replace('%','_').replace('#','_').replace('?','_')}.mpeg', 'wb')
        f.write(r.content)
        f.close
        return 'content_mpeg'
    f = open(f'/home/dorbado/content_mpeg/{([a.replace('.','_') for a in (r.url + '/').split('/') if '.' in a][0]).replace('%','_').replace('#','_').replace('?','_')}.mpeg', 'wb')
    f.write(r.content)
    f.close

def criar_mp4(r,pastas):
    if 'content_mp4' not in pastas:
        os.mkdir('/home/dorbado/content_mp4/')
        return 'content_mp4'
    f = open(f'/home/dorbado/content_mp4/{([a.replace('.','_') for a in (r.url + '/').split('/') if '.' in a][0]).replace('%','_').replace('#','_').replace('?','_')}.mp4', 'wb')
    f.write(r.content)
    f.close

def criar_json(r,pastas):
    if 'content_json' not in pastas:
        os.mkdir('/home/dorbado/content_json/')
        f = open(f'/home/dorbado/content_json/{([a.replace('.','_') for a in (r.url + '/').split('/') if '.' in a][0]).replace('%','_').replace('#','_').replace('?','_')}.json', 'wb')
        f.write(r.content)
        f.close
        return 'content_json'
    f = open(f'/home/dorbado/content_json/{([a.replace('.','_') for a in (r.url + '/').split('/') if '.' in a][0]).replace('%','_').replace('#','_').replace('?','_')}.json', 'wb')
    f.write(r.content)
    f.close

def criar_xml(r,pastas):
    if 'content_xml' not in pastas:
        os.mkdir('/home/dorbado/content_xml/')
        f = open(f'/home/dorbado/content_xml/{([a.replace('.','_') for a in (r.url + '/').split('/') if '.' in a][0]).replace('%','_').replace('#','_').replace('?','_')}.xml', 'wb')
        f.write(r.content)
        f.close
        return 'content_xml'
    f = open(f'/home/dorbado/content_xml/{([a.replace('.','_') for a in (r.url + '/').split('/') if '.' in a][0]).replace('%','_').replace('#','_').replace('?','_')}.xml', 'wb')
    f.write(r.content)
    f.close

def criar_pdf(r,pastas):
    if 'content_pdf' not in pastas:
        os.mkdir('/home/dorbado/content_pdf/')
        f = open(f'/home/dorbado/content_pdf/{([a.replace('.','_') for a in (r.url + '/').split('/') if '.' in a][0]).replace('%','_').replace('#','_').replace('?','_')}.pdf', 'wb')
        f.write(r.content)
        f.close
        return 'content_pdf'
    f = open(f'/home/dorbado/content_pdf/{([a.replace('.','_') for a in (r.url + '/').split('/') if '.' in a][0]).replace('%','_').replace('#','_').replace('?','_')}.pdf', 'wb')
    f.write(r.content)
    f.close