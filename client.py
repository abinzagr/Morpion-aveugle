from grid import *
import socket

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

s_client = socket.socket(socket.AF_INET6,socket.SOCK_STREAM,proto=0)
s_client.connect(('',12345))

grids = [grid(), grid()]
joueur = "" # Type de joueur
rcvspect = "" # Coup joué reçu par spectateur
s1 = s2 = null = 0 # Score
replay = 1 # Booleen pour rejouer

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
		first_shot = s_client.recv(1024).decode()
		grids[0].play(1,int(first_shot))

	if joueur != "adversaire deconnecte":
		i = 0
		grids[1].display()
		while grids[0].gameOver() == -1:
			if joueur != "spectateur":
				shot = -1
				if joueur == "premier joueur": # Numéro du joueur actif
					j = 1
				else:
					j = 2
				# Joueur actif
				while shot < 0 or shot >= NB_CELLS:
					shot = int(input ("Quelle case allez-vous jouer ? "))
					if grids[0].cells[shot] != EMPTY:
						print("Case %d occupée" %shot)
						grids[1].cells[shot] = grids[0].cells[shot]
						shot = -1
					else:
						grids[0].play(j, shot)
						grids[1].play(j, shot)
					grids[1].display()
				s_client.send(str(shot).encode())
				displayWinner(grids[0])

				# Joueur passif
				if j == 1: # Numéro du joueur passif
					j = 2
				else:
					j = 1
				shot = s_client.recv(1024).decode()		
				grids[0].play(j,int(shot))
				displayWinner(grids[0])		
			else:   # Spectateur
				rcvspect = s_client.recv(1024).decode()
				r = int(rcvspect)
				if r >= 0 and r < NB_CELLS:
					if i%2 == 0:
						grids[0].play(1,r)
					else:
						grids[0].play(2,r)
					grids[0].display()
					i += 1
				displayWinner(grids[0])									
	else:	
		print("Adversaire déconnecté.")

	if joueur!="spectateur":
		replay=int(input ("Voulez vous rejouer une partie ? Taper 1 pour 'Oui' ou un autre chiffre pour 'Non' "))
	else:
		replay=int(input ("Voulez vous observer une nouvelle partie ? Taper 1 pour 'Oui' ou un autre chiffre pour 'Non'"))

s_client.close()
