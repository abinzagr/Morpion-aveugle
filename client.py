#client.py

from grid import *
import socket
s_client = socket.socket(socket.AF_INET6,socket.SOCK_STREAM,proto=0)
s_client.connect(('',12345))
grids = [grid(), grid()]
joueur="" # Nom joueur / machine
rcvspect="" # Nom spectateur ? N° ?
i=0
s1=s2=null=0 # Score
replay=1 # Booleen pour rejouer
joueur=s_client.recv(1024).decode()
if(joueur=="spectateur"):
	print(joueur)
if joueur=="premier joueur":
	print("En attente d'un Adversaire...")
	data=s_client.recv(1024)
	grids[0].play(2,int(data))
if joueur!="spectateur":	
	grids[1].display()
while True :		
	if(replay==1):
		if(joueur!="Adversaire Deconnecté"):
			while grids[0].gameOver() == -1:
				shot = -1
				if(joueur!="spectateur"):
					while shot <0 or shot >=NB_CELLS:
						shot = int(input ("quelle case allez-vous jouer ?"))
						#print("cells",grids[0].cells[shot])
						if (grids[0].cells[shot] != EMPTY):
							print("Case occupée %d" %shot)
							grids[1].cells[shot] = grids[0].cells[shot]
							grids[1].display()
							shot=-1
						else:
							grids[0].play(1,shot)
							grids[1].play(1, shot)
							grids[1].display()
					s_client.send(str(shot).encode())
					if grids[0].gameOver() != -1: # Pourquoi en deux fois ?
						print("game over")
						grids[0].display()
						if grids[0].gameOver() == 1:
							print("You win !")
						elif grids[0].gameOver() == 2:
							print("You lose !")
						else:
							print("match nul !")
					
					joueur=s_client.recv(1024).decode()		
					grids[0].play(2,int(joueur))
					#grids[1].play(2,int(joueur))
					#grids[1].display()
					if grids[0].gameOver() != -1: # Pourquoi en deux fois ?
						print("game over")
						grids[0].display()
						if grids[0].gameOver() == 1:
							print("You win !")
						elif grids[0].gameOver() == 2:
							print("You lose !")
						else:
							print("match nul !")
					
				else:
					#grids[0].display()
					
					rcvspect=s_client.recv(1024).decode()
					r=int(rcvspect)
					if(r>=0 and r<9): # i ?
						if(i%2==0):
							grids[0].play(1,int(rcvspect))
							grids[0].display()
						else:
							grids[0].play(2,int(rcvspect))
							grids[0].display()
						i+=1
					if grids[0].gameOver() != -1:
						print("game over")
						grids[0].display()
						if grids[0].gameOver() == 1:
							s1+=1
							print("Joueur 1 win !")
						elif grids[0].gameOver() == 2:
							s2+=1
							print("Joueur 2 win!")
							null+=1
						else:
							print("match nul !")									
		else:	
			print("Adversaire deconnecte,vous avez gagne")
		
		print("Partie termine")
		replay=int(input ("voulez vous rejouer la partie ? Taper 1 pour 'Oui' ou autre chiffre pour 'Non' "))
		print(replay)
		if(replay!=1):
			break
if(replay==1):
	if joueur=="premier joueur":
		#print("En attente d'un Adversaire...")
		data=s_client.recv(1024)
		grids[0].play(2,int(data))

					
	
s_client.close()
