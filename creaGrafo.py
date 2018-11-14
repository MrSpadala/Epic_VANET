from visual import *

p = open("grafi/Luxembourg/pos/pos_time27100Tper50.txt", "r")
for i in p:
	print(i)
	d= i.split(' ')
	sphere(pos=vector(float(d[2]),float(d[3]),0), radius=20)

a = open("grafi/Luxembourg/adj/adj_time27100Tper50.txt", "r")
adi = []
for l in a:
	adi.append([int(n) for n in l.split(' ')])   #get the value as an int
	
print(adi[0][1])
