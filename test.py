import os, hashlib


f = open('Projeto/STORAGE_SERVER/teste.txt', 'r')

client = f.read(11)
f.close()

f = open('Projeto/STORAGE_CLIENT/teste.txt', 'r')

server = f.read(11)
f.close()

client_encode = hashlib.md5(client.encode("utf-8")).hexdigest()
server_encode = hashlib.md5(server.encode("utf-8")).hexdigest()

client = (int(client_encode, 16)).to_bytes(16, "big")
server = int(server_encode, 16)

print(int.from_bytes(client), server)
print()
