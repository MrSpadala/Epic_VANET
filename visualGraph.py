import vpython as vp
#Inserisce le auto nel grafico e ritorna un dizionario che associa
#ogni pallina alla targa dell'auto corrispondente
def displayCars(cars):
	balls = {}
	for c in cars:
		balls[c.plate] = vp.sphere(pos=vp.vector(c.pos[0], c.pos[1], 0), radius=100)
	return balls