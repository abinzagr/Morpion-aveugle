#serveur.py

import socket,select,threading,sys
from grid import *

#notif connexion d'un client aux autres clients	
def notif_connet_joueur(sock,message) :
	if socket != server_socket and socket != sock:
            try:
                print(message)
                socket.send(message.encode('UTF-8'))
            except:
                sock.close()
                list_joueur.remove(sock)

#envoie grille à un joueur



list_joueur = []
#list_observateur =[]
server_socket = socket.socket(socket.AF_INET6,socket.SOCK_STREAM,proto=0)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind (('', 12345)) 
server_socket.listen(1)
list_joueur.append(server_socket)

while 1:
	#verification si un joueur souhaite se connecter + ajout à la liste 
	read_sockets, write_sockets, error_sockets = select.select(list_joueur, [], [])
	for sock in read_sockets:
		if sock == server_socket:
			sockfd, addr = server_socket.accept()
			list_joueur.append(sockfd)
			print("Client (" + str(addr[1]) + ") connected")
			if(len(list_joueur)==2):
				sockfd.send('premier joueur'.encode())
			elif(len(list_joueur)==3):
				sockfd.send('second joueur'.encode())
			else:
				sockfd.send('spectateur'.encode())
		else:
			try:
				mesg = sock.recv(1024).decode()
			except ConnectionResetError:
				print("connexion perdue")
				mesg=''
			if len(mesg) == 0:	
				list_joueur.remove(sock)
				if range(len(list_joueur))==2:
					list_joueur[1].send('Adversaire Deconnecté'.encode())
				sock.close()
			else:
				for i in range(len(list_joueur)):
                                        #Le message est envoyer à tous les joueurs et pas à celui qui l'a envoyé
                                        if list_joueur[i] != server_socket and list_joueur[i] != sock:
                                                list_joueur[i].send(mesg.encode())
						
						
server_socket.close()
