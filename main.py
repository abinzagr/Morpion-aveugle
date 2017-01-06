#!/usr/bin/python3

import socket, select, sys, time, random
from grid import *

def displayWinner(grid, score):
	if grid.gameOver() != -1:
		print("Partie terminée.")
		grid.display()
		if grid.gameOver() == 1:
			print("Joueur 1 gagne !")
			score[0] += 1
		elif grid.gameOver() == 2:
			print("Joueur 2 gagne !")
			score[1] += 1
		else:
			print("Match nul !")
			score[2] += 1
		return 0
	return -1

if len(sys.argv) == 1:
	list_joueur = []
	server_socket = socket.socket(socket.AF_INET6,socket.SOCK_STREAM,proto=0)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((socket.gethostname(), 12345))
	server_socket.listen(5)
	list_joueur.append(server_socket)
	J1 = 0
	J2 = 0

	while True:
		# Attente connexion d'un joueur + ajout à la liste 
		read_sockets, write_sockets, error_sockets = select.select(list_joueur, [], [])
		for sock in read_sockets:
			if sock == server_socket: # Attribution joueur/spectateur
				sockfd, addr = server_socket.accept()
				list_joueur.append(sockfd)
				print("Client (" + str(addr[1]) + ") connecté.")
				if J1 == 0:
					sockfd.send('premier joueur'.encode())
					sockfd
					J1 = sockfd
				elif J2 == 0:
					sockfd.send('second joueur'.encode())
					list_joueur[1].send('second joueur'.encode())
					J2 = sockfd
				else:
					sockfd.send('spectateur'.encode())
			else:
				try:
					mesg = sock.recv(1024).decode()
				except ConnectionResetError:
					print("Connexion perdue.")
				if len(mesg) == 0:
					print("Connexion perdue.")
					if sock == list_joueur[1] or sock == list_joueur[2]:
						if sock == J1:
							J1 = 0
						if sock == J2:
							J2 = 0
						for i in range(1, len(list_joueur)):
							if list_joueur[i] != sock:
								list_joueur[i].send('adversaire deconnecte'.encode())
					list_joueur.remove(sock)
					sock.close()
				else: # Envoi coup joué + lancement d'une nouvelle partie
					if mesg == "rejouer":
						if sock == J1:
							J1 = 0
						if sock == J2:
							J2 = 0
						list_joueur.remove(sock)
						sock.close()
					else:
						for i in range(1, len(list_joueur)):
							if list_joueur[i] != sock:
								list_joueur[i].send(mesg.encode())
	server_socket.close()
elif len(sys.argv) == 2:
	joueur = "" # Type de joueur
	score = [0,0,0] # Tableau des scores
	replay = "o" # Caractère pour rejouer


	while replay == "o" or replay == "O":
		replay = ""
		entry = ""
		while entry != "o" and entry != "O" and entry != "n" and entry != "N":
			entry = input("Voulez-vous jouer seul ? O/N ")
		if entry == "O" or entry == "o":
			alone = 1
			grids = [grid(), grid(), grid()]
			current_player = J1
			grids[J1].display()
			while grids[0].gameOver() == -1:
				if current_player == J1:
					shot = -1
					while shot <0 or shot >=NB_CELLS:
						shot = int(input ("Quelle case allez-vous jouer ? "))
				else:
					shot = random.randint(0,8)
					while grids[current_player].cells[shot] != EMPTY:
						shot = random.randint(0,8)
				if (grids[0].cells[shot] != EMPTY):
					grids[current_player].cells[shot] = grids[0].cells[shot]
				else:
					grids[current_player].cells[shot] = current_player
					grids[0].play(current_player, shot)
					current_player = current_player%2+1
				if current_player == J1:
					grids[J1].display()
			print("game over")
			grids[0].display()
			if grids[0].gameOver() == J1:
				print("Vous avez gagné !")
			else:
				print("Vous avez perdu.")
			while replay != "o" and replay != "O" and replay != "n" and replay != "N":
				replay = input ("Voulez vous rejouer une partie ? O/N ")
		elif entry == "N" or entry == "n":
			alone = 0
			s_client = socket.socket(socket.AF_INET6,socket.SOCK_STREAM,proto=0)
			s_client.connect((sys.argv[1],12345))
			j = 1
			grids = [grid(), grid()]
			joueur = s_client.recv(1024).decode()
			if joueur == "spectateur":
				print("Vous êtes spectateur.")
			if joueur == "premier joueur":
				print("Vous êtes le Joueur 1.")
				print("En attente d'un Adversaire...")
				tmp = s_client.recv(1024).decode()
			if joueur == "second joueur":
				print("Vous êtes le Joueur 2.")
				entry = s_client.recv(1024).decode()
				if entry != "adversaire deconnecte":
					first_shot = int(entry)
					grids[0].play(1, first_shot)

			i = 0
			grids[1].display()
			while displayWinner(grids[0], score) == -1 and entry != "adversaire deconnecte":
				if joueur != "spectateur":
					shot = -1
					valid_shot = 1
					if joueur == "premier joueur": # Numéro du joueur actif
						j = 1
					else:
						j = 2
					# Joueur actif
					while valid_shot != 0:
						while shot < 0 or shot >= NB_CELLS:
							entry = input ("Quelle case allez-vous jouer ? (0-8) ")
							try:
								shot = int(entry)
							except ValueError:
								print("Entrez un chiffre entre 0 et 8")
						if grids[0].cells[shot] != EMPTY:
							print("Case ", shot, " occupée")
							grids[1].cells[shot] = grids[0].cells[shot]
							shot = -1
						else:
							grids[0].play(j, shot)
							grids[1].play(j, shot)
							valid_shot = 0
						grids[1].display()
					s_client.send(str(shot).encode())

					# Joueur passif
					if grids[0].gameOver() == -1:
						if j == 1: # Numéro du joueur passif
							j = 2
						else:
							j = 1
						entry = s_client.recv(1024).decode()
						if entry != "adversaire deconnecte":
							shot = int(entry)
							grids[0].play(j, shot)
			
				else:   # Spectateur
					entry = s_client.recv(1024).decode()
					if entry != "adversaire deconnecte":
						rcvspect = int(entry)
						if rcvspect >= 0 and rcvspect < NB_CELLS:
							if i%2 == 0:
								grids[0].play(1, rcvspect)
							else:
								grids[0].play(2, rcvspect)
							grids[0].display()
							i += 1

			while replay != "o" and replay != "O" and replay != "n" and replay != "N":
				if joueur != "spectateur":
					replay = input ("Voulez-vous rejouer une partie ? O/N ")
				else:
					replay = input ("Voulez-vous observer une nouvelle partie ? O/N ")
			if replay == "o" or replay == "O":
				s_client.send('rejouer'.encode())
				s_client.close()

	print("Tableau des scores :")
	for k in range(2):
		print("Joueur ", k+1, " : ", score[k])
	print("Match nul : ", score[2])

	if alone == 0:
		s_client.close()
else:
	sys.exit()

