import socket,select,threading,sys
from grid import *

list_joueur = []
server_socket = socket.socket(socket.AF_INET6,socket.SOCK_STREAM,proto=0)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind (('', 12345)) 
server_socket.listen(1)
list_joueur.append(server_socket)

while True:
	# Attente connexion d'un joueur + ajout à la liste 
	read_sockets, write_sockets, error_sockets = select.select(list_joueur, [], [])
	for sock in read_sockets:
		if sock == server_socket: # Attribution joueur/spectateur
			sockfd, addr = server_socket.accept()
			list_joueur.append(sockfd)
			print("Client (" + str(addr[1]) + ") connecté.")
			if len(list_joueur) == 2:
				sockfd.send('premier joueur'.encode())
			elif len(list_joueur) == 3:
				sockfd.send('second joueur'.encode())
				list_joueur[1].send('second joueur'.encode())
			else:
				sockfd.send('spectateur'.encode())
		else:
			try:
				mesg = sock.recv(1024).decode()
			except ConnectionResetError:
				print("Connexion perdue.")
			if len(mesg) == 0:
				list_joueur.remove(sock)
				if len(list_joueur) == 2:
					list_joueur[1].send('adversaire deconnecte'.encode())
					print("Adversaire déconnecté")
				sock.close()
			else: # Envoi coup joué + lancement d'une nouvelle partie
				if mesg == "replay":
					sock.send(mesg.encode())
					mesg = sock.recv(1024).decode()
					sock.send(mesg.encode())
					if mesg == "second joueur":
						list_joueur[1].send(mesg.encode())
				else:
					for i in range(1, len(list_joueur)):
						if list_joueur[i] != sock:
							list_joueur[i].send(mesg.encode())
server_socket.close()
