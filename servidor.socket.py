#!/usr/bin/python3
import os
import os.path
import socket
import subprocess

HOST = '192.168.0.177'
PORT = 40000
TAM_MSG = 1024
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv = (HOST, PORT)
sock.bind(serv)
sock.listen(50)
while True:
    try:
        con, cliente = sock.accept()
    except: break
    pid = os.fork()
    if pid == 0:
        print('Cliente conectado', cliente)
        while True:
            msg = con.recv(TAM_MSG)
            if not msg: break
            msg = msg.decode().split()
            
            if msg[0].lower() == 'ping':
                endereco = ''.join(msg[1:])
                result = subprocess.run(['ping','-c', '4', endereco], stdout=subprocess.PIPE)
                comando = result.stdout.decode('utf-8')
                div = comando.split()
                if 'ttl' in comando:
                    con.send(str.encode('{}\n+WORK'.format(comando)))
                else:
                    con.send(str.encode('-WRONG\nHost não encontrado ou incorreto\n'))
            # CD
            elif msg[0].lower() == 'cd':
               diretorio = ''.join(msg[1:])
               try:
                   caminho = ('./'+diretorio+'/')
                   dirc = os.chdir(caminho)
                   con.send(str.encode('200+WORK\n'))
               except FileNotFoundError:
                   con.send(str.encode('-WRONG Diretório não encontrado\n'))
            
            # LS 
            elif msg[0].lower() == 'ls':
                    if len(msg) > 1:
                        arq = msg[1]
                        result = subprocess.run(['ls', arq], stdout=subprocess.PIPE)
                        comando = result.stdout.decode()
                        con.send(str.encode(comando))
                        if not os.path.exists(arq):
                            con.send(str.encode('404-WRONG\nDiretório Não Encontrado!'))
                    elif len(msg) == 1:
                        result = subprocess.run(['ls'], stdout=subprocess.PIPE)
                        comando = result.stdout.decode('utf-8')
                        con.send(str.encode(comando))

            elif msg[0].lower() == 'remove':
                try:
                    arq = os.remove(msg[1])
                    con.send(str.encode('Removido'))
                except OSError as error:
                    con.send(str.encode('Arquivo ou Diretorio não pode ser removido'))
            
            # QUIT
            elif msg[0].lower() == 'quit':
                break

        print('Cliente desconectado', cliente)
        con.close()
        break
    else:
        con.close()
sock.close()
