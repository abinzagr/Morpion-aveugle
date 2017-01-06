from grid import *
import socket
import sys
import signal

def signal_perte_connexion(signal, frame):
	s_client.send('perdu'.encode())
	sys.exit(0)
	
signal.signal(signal.SIGINT, signal_perte_connexion)	
	
def displayWinner(grid):
	if grid.gameOver() != -1:
		print("Partie terminée.")
		grid.display()
		if grid.gameOver() == 1:
			print("Joueur 1 gagne !")
		elif grid.gameOver() == 2:
			print("Joueur 2 gagne !")
			
		else:
			print("Match nul !")
		return 0
	return -1

s_client = socket.socket(socket.AF_INET6,socket.SOCK_STREAM,proto=0)
s_client.connect(('',12345))

grids = [grid(), grid()]
joueur = "" # Type de joueur
s1 = s2 = null = 0 # Score (nécessite replay fonctionnel)
replay = 1 # Booleen pour rejouer
connex=""
while replay == 1:
	joueur = s_client.recv(1024).decode()
	if joueur == "spectateur":
		print("Vous êtes spectateur.")
	if joueur == "premier joueur":
		print("Vous êtes le Joueur 1.")
		print("En attente d'un Adversaire...")
		adv_recv = s_client.recv(1024).decode()
	if joueur == "second joueur":
		print("Vous êtes le Joueur 2.")
		connex = s_client.recv(1024).decode()
		print(connex)
		if connex == "adversaire deconnecte"	:
			sys.exit(0)
		first_shot = int(s_client.recv(1024).decode())
		grids[0].play(1, first_shot)

	
	i = 0
	grids[1].display()
	while displayWinner(grids[0]) == -1:
		if joueur != "spectateur":
			shot = -1
			valid_shot = 1
			if joueur == "premier joueur": # Numéro du joueur actif
				j = 1
			else:
				j = 2
			# Joueur actif
			while valid_shot != 0:
				entry = ""
				while shot < 0 or shot >= NB_CELLS:
					entry = input ("Quelle case allez-vous jouer ? (0-8) ")
					try:
						shot = int(entry)
					except ValueError:
						print("Entrez un chiffre entre 0 et 8")
				if grids[0].cells[shot] != EMPTY:
					print("Case %d occupée" %shot)
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

				shot = int(entry)
				grids[0].play(j, shot)
	
		else:   # Spectateur
			rcvspect = int(s_client.recv(1024).decode())
			if rcvspect >= 0 and rcvspect < NB_CELLS:
				if i%2 == 0:
					grids[0].play(1, rcvspect)
				else:
					grids[0].play(2, rcvspect)
				grids[0].display()
				i += 1									

	if joueur!="spectateur":
		replay=int(input ("Voulez vous rejouer une partie ? Taper 1 pour 'Oui' ou un autre chiffre pour 'Non' "))
	else:
		replay=int(input ("Voulez vous observer une nouvelle partie ? Taper 1 pour 'Oui' ou un autre chiffre pour 'Non' "))

s_client.close()
