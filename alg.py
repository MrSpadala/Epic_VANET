########### BISOGNA DEFINIRE LE FUNZIONI DI BROADCAST E DI RICEZIONE (COME SI INVIANO I MESSAGGI? SOCKET O LE FUNZIONI CI VENGONO FORNITE?)

#msg:
#	num_seq
#	xs
#	ys
#	xr
#	yr
#	h
#	ttl

import multiprocessing
import time


def get_positions(msg_positions):
	i=0
    while True:
		if read_message() == msg and (msg[xr], msg[yr]) not in msg_positions:
			msg_positions[i]=(msg[xr], msg[yr])								# qui acquisiamo le posizioni
			i++																# da cui arrivano i messaggi



def evaluate_positions(msg_positions):
	quads = [0,0,0,0]			# flags dei quadranti: 0 quadrante inesplorato, 1 quadrante esplorato
	my_pos = get_my_pos			# abbiamo scelto quadranti divisi da una X dalla nostra posizione
	for i in range(0,msg_positions.len):
		if quads[0]!=1
			if i[0]>my_pos[0] and i[1] is in range(my_pos[1]-(abs((my_pos[0]-i[0])/2)), my_pos[1]-(abs((my_pos[0]-i[0])/2))):		# X > myX	dx
				quads[0]=1

		if quads[1]!=1
			if i[1]>my_pos[1] and i[0] is in range(my_pos[0]-(abs((my_pos[1]-i[1])/2)), my_pos[0]-(abs((my_pos[1]-i[1])/2))):		# Y > myY	su
				quads[1]=1

		if quads[2]!=1
			if i[0]<my_pos[0] and i[1] is in range(my_pos[1]-(abs((my_pos[0]-i[0])/2)), my_pos[1]-(abs((my_pos[0]-i[0])/2))):		# X < myX	sx
				quads[2]=1

		if quads[3]!=1
			if i[1]<my_pos[1] and i[0] is in range(my_pos[0]-(abs((my_pos[1]-i[1])/2)), my_pos[0]-(abs((my_pos[1]-i[1])/2))):		# Y < myY	giù
				quads[3]=1
	if quads==[1,1,1,1]:
		return False
	else:
		return True



def foo(msg, node, tmax):

	# Scadenza del messaggio
	if msg.ttl==0:
		return

 	# Calcolo il tempo di attesa di ritrasmissione in base alla distanza
	# distance = dist(get_pos(), (msg.xr, msg.yr))
	dAS = dist(get_my_pos(), (msg.xs, msg.ys))


	# inizializzare R
	t = tmax * (1-(dAS / R))


	manager = multiprocessing.Manager()

	msg_positions = manager.dict()		#msg_position diventa un dizionario

	p = multiprocessing.Process(target=get_positions, args=(msg_positions,))	# facciamo partire in parallelo la funzione per acquisire le posizioni dei vicini che hanno già il messaggio e il timer
	p.start()
	print "Waiting for " + t + " sec"
	time.sleep(t)
	p.terminate()

	# conosciamo le posizioni in msg_positions

 	do_broadcast = evaluate_positions(msg_positions)

 	if do_broadcast:
		broadcast_msg(msg)

	msg_positions=[]
