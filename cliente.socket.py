#!/usr/bin/env python3
import socket
import sys

TAM_MSG = 1024         # Tamanho do bloco de mensagem
HOST = '192.168.0.177'     # IP do Servidor
PORT = 40000           # Porta que o Servidor escuta

if len(sys.argv) > 1:
    HOST = sys.argv[1]
print('Servidor:', HOST+':'+str(PORT)) 
serv = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect (serv)
print('Para sair use QUIT, Ctrl+D ou CTRL+C\n')
while True:
	try:
		cmd = input('JAP> ')
	except:
		cmd = 'QUIT'
		break
	
	sock.send(str.encode(cmd))
	dados = sock.recv(TAM_MSG)

	if not dados: break 
	msg_status = dados.decode().split('\n')

	cmd = cmd.split()

	if cmd[0].lower() == 'ping':
		for linha in msg_status:
			print(linha)