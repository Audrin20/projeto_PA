#!/usr/bin/python3
import os
import socket
import subprocess
import sys

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

            if msg[0].lower() == 'cd':
               diretorio = ''.join(msg[1:])
               try:
                   caminho = ('./'+diretorio+'/')
                   dirc = os.chdir(caminho)
                   con.send(str.encode('+WORK\n'))
               except FileNotFoundError:
                   con.send(str.encode('-WRONG Diretório não encontrado\n'))

            # FALTA TERMINAR

            if msg[0].lower() == 'ssh':
                server = msg[1]
                print(msg)
                result = subprocess.run(['sshpass','-p','root','ssh', server], stdout=subprocess.PIPE)
                a = result.stdout.decode()
                con.send(str.encode(a))
            # FALTA TERMINAR

            if msg[0].lower() == 'ls':
                path = msg[1]
                arq = [f for f in listdir(path) if isfile(join(path, f))]
                con.send(str.encode(arq))
            if msg[0].lower() == 'quit':
                break
        print('Cliente desconectado', cliente)
        con.close()
        break
    else:
        con.close()
sock.close()
