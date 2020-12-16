#!/usr/bin/python3

import socket
import sys

HOST = 'localhost'
PORT = 40000

if len(sys.argv) > 1:
    HOST = sys.argv[1]

print('Servidor:', (HOST, PORT))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv = (HOST, PORT)
sock.connect(serv)
while True:
    try:
        msg = input('Mensagem: ')
    except: break
    sock.send(str.encode(msg))
    msg = sock.recv(1024)
    if not msg: break
    print('Recebido:', msg.decode())
sock.close()

