from visual import *
#import alg
import random
import math
import time
import thread



#Calcolo la distanza, se e minore di R disegno freccia e rimando broadcast
#p e la posizione attuale
def broad_msg(balls, r, p):
	for b in balls:
		if b.color!=color.red:
			if dist(p, b.pos) < r:
				b.color= color.red
				arrow(pos=p, axis=(b.x - p.x, b.y - p.y, 0), shaftwidth=0.1, color=color.green)
				time.sleep(0.5)
				thread.start_new_thread(broad_msg, (balls, r, b.pos))


def dist(v1, v2):
	distx = abs(v1.x - v2.x)
	disty = abs(v1.y - v2.y)
	return sqrt(distx*distx + disty*disty)

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
for i in range(-40,50,20):
	for j in range(-40,50,20):
		for r in range(i-4, i, 2):
			for c in range(-40,50, 2):
				if r>-30:
					if random.randrange(1, 50) < 2:
						balls.append(sphere(pos=vector(r,c,0), radius=0.6))
		for r in range(-40,50, 2):
			for c in range(i-4, i, 2):
				if c>-30:
					if random.randrange(1, 50) < 2:
							balls.append(sphere(pos=vector(r,c,0), radius=0.6))

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
message = "Infected"
print(str(loc)+" says: " + message)
broad_msg(balls, 20, loc)
