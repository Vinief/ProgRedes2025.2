import os

print(os.getcwd())

def caminho(path):
    raiz = '../STORAGE_SERVER'
    
    caminho_real = os.path.realpath(path)

    if (caminho_real).startswith(raiz):
        return True
    else:
        return False 