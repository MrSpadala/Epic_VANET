import collections

#msg ha i campi descritti sopral'algoritmo
# msg.Vector è una list di tuple ( veicolo , veicolo.dist )

def sortSecond(val): 
    return val[1]  
    
def setBkTimer(value):
	# settiamo un timer di valore value
	# chiamiamo la backup routine (booooh)

def RN_election(msg):
	msg.Vrx.dist = distance(msg.Vrx.pos, msg.NRP)
	msg.Vector.append(msg.Vrx, msg.Vrx.dist)
	
	##########preso dal nostro evaluate position##############
	neighbor_positions = []   #positions of neighbors cars
		for c, i in zip(msg.Vrx.adj, range(len(msg.Vrx.adj))):
			if c == 1:
				#Ho preso la macchina corrispondente
				obj = msg.Vrx.sim.getCar(i)
				if obj != None:
					neighbor_positions.append(obj.pos)
	##########################################################

	
	for v in neighbor_positions:
		v.dist = distance(v.pos, msg.NRP)
		msg.Vector.append(v, v.dist)
	msg.Vector.sort(key=sortSecond)	# sort in base a dist
	if msg.Vector[0]==Vrx:
		return True		# a questo punto broadcastiamo
	else:
		setBkTimer(msg.Td*msg.Vector.index(Vrx))
		return False
	
