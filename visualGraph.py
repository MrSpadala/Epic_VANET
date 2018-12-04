import vpython as vp
#Inserisce le auto nel grafico e ritorna un dizionario che associa
#ogni pallina alla targa dell'auto corrispondente
def displayCars(cars):
	balls = {}
	for c in cars:
		balls[cars[c].plate] = vp.sphere(pos=vp.vector(cars[c].pos[0], cars[c].pos[1], 0), radius=10)
	return balls

def firstInfection(balls):
	flag = 0
	while True:
		m=vp.scene.waitfor('click')
		loc = m.pos
		loc.z = 0
		print(loc)
		for k in balls:
			if balls[k].pos.x<loc.x+100 and balls[k].pos.y<loc.y+100 and balls[k].pos.x>loc.x-100 and balls[k].pos.y>loc.y-100:
				balls[k].color = vp.color.red
				flag = 1
				infectedPlate= k
				break
		if flag:
			break
	return k