# messaggio.Vector è una list di tuple ( veicolo , veicolo.dist )

def sortSecond(val):
    return val[1]

def setBkTimer(value):
	# settiamo un timer di valore value
	# chiamiamo la backup routine (booooh)

def RN_election(msg):
	messaggio.Vrx.dist = distance(messaggio.Vrx.pos, messaggio.NRP)
	messaggio.Vector.append(messaggio.Vrx, messaggio.Vrx.dist)

	##########preso dal nostro evaluate position##############
	neighbor_positions = []   #positions of neighbors cars
		for c, i in zip(messaggio.Vrx.adj, range(len(messaggio.Vrx.adj))):
			if c == 1:
				#Ho preso la macchina corrispondente
				obj = messaggio.Vrx.sim.getCar(i)
				if obj != None:
					neighbor_positions.append(obj.pos)
	##########################################################


	for v in neighbor_positions:
		v.dist = distance(v.pos, messaggio.NRP)
		messaggio.Vector.append(v, v.dist)
	messaggio.Vector.sort(key=sortSecond)	# sort in base a dist
	if messaggio.Vector[0]==Vrx:
		return True		# a questo punto broadcastiamo
	else:
		setBkTimer(messaggio.Td*messaggio.Vector.index(Vrx))
		return False
