def get_adj(balls, raggio):
    adj=[]
    for b in balls:
        if abs(b.pos - loc) < raggio:
            adj.append(b)


def dist(c1, c2):
	distx = abs(c1.pos[0] - c2.pos[0])
	disty = abs(c1.pos[1] - c2.pos[1])
	return sqrt(distx*distx + disty*disty)


def evaluate_positions(messages, my_pos):   # 1 messaggio solo  ## valuta se mandare in broadcast o no
	quads = [0,0,0,0]			# flags dei quadranti: 0 quadrante inesplorato, 1 quadrante esplorato
								# abbiamo scelto quadranti divisi da una X dalla nostra posizione
	for m in messages:
		if quads[0]!=1:
			if m.emit[0]>my_pos[0] and  my_pos[1]-(abs((my_pos[0]-m.emit[0])/2)) <= m.emit[1] <= my_pos[1]-(abs((my_pos[0]-m.emit[0])/2)):		# X > myX	dx
				quads[0]=1

		if quads[1]!=1:
			if m.emit[1]>my_pos[1] and (my_pos[0]-(abs((my_pos[1]-m.emit[1])/2)) <= m.emit[0] <= my_pos[0]-(abs((my_pos[1]-m.emit[1])/2))):		# Y > myY	su
				quads[1]=1

		if quads[2]!=1:
			if m.emit[0]<my_pos[0] and (my_pos[1]-(abs((my_pos[0]-m.emit[0])/2)) <= m.emit[1] <= my_pos[1]-(abs((my_pos[0]-m.emit[0])/2))):		# X < myX	sx
				quads[2]=1

		if quads[3]!=1:
			if m.emit[1]<my_pos[1] and (my_pos[0]-(abs((my_pos[1]-m.emit[1])/2)) <= m.emit[0] <= my_pos[0]-(abs((my_pos[1]-m.emit[1])/2))):		# Y < myY	giu
				quads[3]=1


	print("Decidendo...")

	if quads==[1,1,1,1]:
		return False
	else:
		return True
