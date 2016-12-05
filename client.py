#client.py

from grid import *
import socket
s_client = socket.socket(socket.AF_INET6,socket.SOCK_STREAM,proto=0)
s_client.connect(('',12345))
grids = [grid(), grid()]
joueur=""
joueur=s_client.recv(1024).decode()
print(joueur)
if joueur=="premier joueur":
	print("En attente d'un Adversaire...")
	data=s_client.recv(1024)
	grids[0].play(2,int(data))
grids[1].display()
while(joueur!="Adversaire Deconnecté"):
	
	while grids[0].gameOver() == -1:
		shot = -1
		while shot <0 or shot >=NB_CELLS:
			while shot <0 or shot >=NB_CELLS:
				shot = int(input ("quelle case allez-vous jouer ?"))
				print("cells",grids[0].cells[shot])
			if (grids[0].cells[shot] != EMPTY):
				print("Case occupée %d" %shot)
				grids[1].cells[shot] = grids[0].cells[shot]
				grids[1].display()
				shot=-1
			else:
				grids[0].play(1,shot)
				grids[1].play(1, shot)
				grids[0].display()
		s_client.send(str(shot).encode())
		if grids[0].gameOver() != -1:
			print("game over")
			grids[0].display()
			if grids[0].gameOver() == 1:
				print("You win !")
			else:
				print("you loose !")
		joueur=s_client.recv(1024).decode()		
		grids[0].play(2,int(joueur))
		grids[1].play(2,int(joueur))
		grids[0].display()
		
	print("Fermeture de la connexion")

s_client.close()
