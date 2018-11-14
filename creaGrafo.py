from visual import *

p = open("grafi/Luxembourg/pos/pos_time27100Tper50.txt", "r")
for i in p:
	print(i)
	d= i.split(' ')
	sphere(pos=vector(float(d[2]),float(d[3]),0), radius=20)
