
import sys
if not "--with-graphics" in sys.argv:
	pass

else:
	import vpython as vp
	#Insert vehicles in the graph and returns a dict associating each
	#ball to the vehicle plate
	palle={}

	#for vpython useful commands see here: vpython.org/contents/docs/display.html
	vp.scene.title= "Visual Test VANET"
	vp.scene.x=0
	vp.scene.y=0
	vp.scene.background=vp.color.gray(0.8)
	vp.scene.width= 1300
	vp.scene.height=900
	vp.scene.center=vp.vector(7000, 4500, 0)

	def displayCars(cars):
		balls = {}
		for c in cars:
			balls[cars[c].plate] = vp.sphere(pos=vp.vector(cars[c].pos[0], cars[c].pos[1], 0), radius=10)
		global palle
		palle = balls
		return balls

	def firstInfection():
		flag = 0
		while True:
			m=vp.scene.waitfor('click')
			loc = m.pos
			loc.z = 0
			print(loc)
			global palle

			for k in palle:
				if palle[k].pos.x<loc.x+10 and palle[k].pos.y<loc.y+10 and palle[k].pos.x>loc.x-10 and palle[k].pos.y>loc.y-10:
					print(k)

					palle[k].color = vp.color.red
					flag = 1
					infectedPlate= k
					break
			if flag:
				break
		return k

	def visualInfect(src, dest):
		global palle
		palle[dest.plate].color=vp.color.red
		palle[src.plate].color=vp.color.blue
		vp.arrow(pos=vp.vector(src.pos[0],src.pos[1],0), axis=vp.vector(dest.pos[0] - src.pos[0], dest.pos[1] - src.pos[1], 0), shaftwidth=1, headwidth=2, headlength=3, color=vp.color.green)
