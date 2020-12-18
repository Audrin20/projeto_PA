#!/usr/bin/env python3
import socket
import sys

TAM_MSG = 1024   
HOST = ''     
PORT = 40000      

if len(sys.argv) > 1:
    HOST = sys.argv[1]

serv = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect (serv)

while True:
	try:
		cmd = input('CMP-> ')
	except:
		cmd = 'QUIT'
		break
	
	sock.send(str.encode(cmd))
	dados = sock.recv(TAM_MSG)

	if not dados: break 
	message = dados.decode().split('\n')

	cmd = cmd.split()

	if cmd[0].lower() == 'ping':
		for linha in message:
			print(linha)
	elif cmd[0].lower() == 'ls':
		for linha in message:
			print(linha)
	elif cmd[0].lower() == 'removearq':
		msg = ''.join(message[0:])
	elif cmd[0].lower() == 'cd':
		print(message[0])
	elif cmd[0].lower() == 'help':
		msg = ''.join(message[0])
		for linha in message:
			print(msg)
	elif cmd[0] == 'quit':
		msg = ''.join(message)
		print(msg)
		break
	else:
		msg = ''.join(message)
		print(f'-WRONG\n{msg}')
		print('Consulte "help"')
