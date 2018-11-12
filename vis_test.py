from visual import *
import random

scene.title= "Visual Test VANET"
scene.x=0 
scene.y=0
scene.width= 900 
scene.height=1000
scene.center=(5,0,0)
scene.background=(0.8, 0.8, 0.8)

#Creo gli edifici (cubi)
for i in range(-40,50,20):
	for j in range(-40,50,20):
		for r in range(i, i+16):
			for c in range(j, j+16):
				box(pos=vector(r,c,0))

#Creo i veicoli (sfere)
balls = []
for i in range(-50,40,5):
	for j in range(-50,40,5):
		for r in range(i+16, i+20, 2):
			for c in range(j+16, j+20, 2):
				if r not in range(i, i+16) and c not in range(j,j+16):
					if random.randrange(1, 10) < 2:
						balls.append(sphere(pos=vector(r,c,0), radius=0.6))

# non commento
for i in range(-40,50,20):
	for j in range(-40,50,20):
		for r in range(i, i+16):
			for c in range(j, j+16):
				for b in balls:
					if b.pos==vector(r,c,0):
						b.visible=False
						del b
						break
#al click evidenzio il veicolo infettato
flag = 0
while True:
        rate(30)
        if scene.mouse.clicked:
                m= scene.mouse.getclick()
                loc = m.pos
                loc.z = 0
                print(loc)
                for b in balls:
                        if b.pos.x<loc.x+1 and b.pos.y<loc.y+1 and b.pos.x>loc.x-1 and b.pos.y>loc.y-1:
                                b.color = color.red
                                flag = 1
                                break
		if flag:
			break
                                

#Parte l'algoritmo di infezione
#TODO
