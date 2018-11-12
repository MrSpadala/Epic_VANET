from visual import *
import random

class Scenario():


	for i in range(-40,50,20):
		for j in range(-40,50,20):
			for r in range(i, i+16):
				for c in range(j, j+16):
					box(pos=vector(r,c,0))

	balls = []
	for i in range(-50,40,5):
		for j in range(-50,40,5):
			for r in range(i+16, i+20, 2):
				for c in range(j+16, j+20, 2):
					if r not in range(i, i+16) and c not in range(j,j+16):
						if random.randrange(1, 10) < 2:
							balls.append(sphere(pos=vector(r,c,0), radius=0.6))


	for i in range(-40,50,20):
		for j in range(-40,50,20):
			for r in range(i, i+16):
				for c in range(j, j+16):
					for b in balls:
						if b.pos==vector(r,c,0):
							b.visible=False
							del b
							break
