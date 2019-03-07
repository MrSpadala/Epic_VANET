import random
from time import sleep
from decimal import Decimal
from collections import deque
from pdb import set_trace
from math import sqrt
from msg import Msg
from enum import Enum
from visualGraph import *



class State(Enum):
	VULNERABLE = 0
	INFECTED = 1
	RECOVERED = 2


def dist(p,q):
	return sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)
def in_range(p,q,radius):  #ritorna se p e q sono distanti meno di 'radius'
	return dist(p,q) < radius


class Car:
	#Costruttore
	def __init__(self, plate, pos, adj):
		self.plate = plate
		self.pos = pos
		self.messages = []
		self.state = State.VULNERABLE
		self.timer_infected = None
		self.adj = adj
		self.sim = None  #simulator object

	def modifyMsg(self, msg, msg_list):
		#Modifico il messaggio con i miei dati
		msg.last_emit = self.pos
		all_emitters = set([self.pos])
		for m in msg_list:
			all_emitters = all_emitters.union(set(m.emitters))
		
		#I update the list of the emitters and if its length exceeds EMITTERS_LIMIT I keep the closest ones
		key = lambda x: dist(x, self.pos)
		all_emitters_srtd = sorted(list(all_emitters), key=key, reverse=True)
		msg.emitters = deque(all_emitters_srtd, maxlen=Msg.EMITTERS_LIMIT)
		
		msg.hop += 1

	def broadMsg(self):
		bcast = self.evaluate_positions2(self.messages, self.pos)
		if (not bcast):
			return
		#manca il controllo delle direzioni

		msg = self.messages[0].clone()  #prendo il primo messaggio della lista, quello che ha generato l'infezione
		self.modifyMsg(msg, self.messages)

		#Se il messaggio è arrivato al limite di hop mi fermo
		if msg.hop == msg.ttl:
			return

		message_sent = False
		for c, i in zip(self.adj, range(len(self.adj))):
			if c == 1:
				#Ho preso la macchina corrispondente
				obj = self.sim.getCar(i)
				if obj == None:
					continue

				if not message_sent:
					message_sent = True
					self.sim.sent_messages += 1

				if not self.sim.no_graphics:
					if obj.state == State.VULNERABLE:
						visualInfect(self, obj)
				obj.infect(msg)

		if not self.sim.no_graphics:
			sleep(0.01)

		self.messages.clear()


	def infect(self, msg):
		#Simulo la perdita di una percentuale di messaggi *in ricezoione*
		if random.random() < Simulator.DROP:
			return

		self.sim.rcv_messages += 1
		#se e' il primo messaggio faccio partire il timer di attesa
		#altrimenti aggiungo solo il messaggio alla lista
		if self.state == State.RECOVERED:   #Se è RECOVERED nessuna infezione ha effetto
			return

		if self.state == State.VULNERABLE:  #Se la macchina ancora non è infettata allora viene infettata e settato il timer
			self.sim.t_last_infected = self.sim.t
			self.sim.n_hop_last_infected = msg.hop
			self.state = State.INFECTED
			self.timer_infected = self.getWaitingTime(msg.last_emit)   #setta il timer di attesa in funzione della distanza dell'emitter
			#decomment to see all timers
			#print("timer_infected set to:", self.timer_infected * Simulator.TIME_RESOLUTION, "seconds")

		self.messages.append(msg)


	def getWaitingTime(self, emit_pos):
		#print(self.pos, emit_pos)
		dAS = dist(self.pos, emit_pos)   #distanza tra me e l'emittente che me lo ha mandato, espressa in metri
		t_dist = Simulator.TMAX*(1 - dAS/Simulator.RMAX)   #tempo di attesa dipendente dalla distanza, espresso in secondi
		t_non_determ = t_dist * random.random()   #tempo di attesa non deterministico in (0, t_dist) secondi

		#tempo finale calcolato con il parametro ALPHA che decide il bilanciamento della componente deterministica e non deterministica.
		#t_final è compreso tra ( (ALPHA)*t_dist , t_dist ) secondi
		t_final = Simulator.ALPHA*t_dist + (1-Simulator.ALPHA)*t_non_determ

		if t_final <= Simulator.TMIN:
			t_final = Simulator.TMIN
		if t_final >= Simulator.TMAX:
			t_final = Simulator.TMAX

		return t_final / Simulator.TIME_RESOLUTION    #ritorna il tempo di attesa espresso nel numero di step da fare al simulatore.

	def evaluate_positions(self, messages, my_pos):   # 1 messaggio solo  ## valuta se mandare in broadcast o no
		quads = [0,0,0,0]			# flags dei quadranti: 0 quadrante inesplorato, 1 quadrante esplorato
									# abbiamo scelto quadranti divisi da una X dalla nostra posizione

		for m in messages:

			if quads[0]!=1:
				if m.last_emit[0]>my_pos[0] and my_pos[1]-(abs((my_pos[0]-m.last_emit[0])/2)) <= m.last_emit[1] <= my_pos[1]-(abs((my_pos[0]-m.last_emit[0])/2)):		# X > myX	dx
					quads[0]=1

			if quads[1]!=1:
				if m.last_emit[1]>my_pos[1] and (my_pos[0]-(abs((my_pos[1]-m.last_emit[1])/2)) <= m.last_emit[0] <= my_pos[0]-(abs((my_pos[1]-m.last_emit[1])/2))):		# Y > myY	su
					quads[1]=1

			if quads[2]!=1:
				if m.last_emit[0]<my_pos[0] and (my_pos[1]-(abs((my_pos[0]-m.last_emit[0])/2)) <= m.last_emit[1] <= my_pos[1]-(abs((my_pos[0]-m.last_emit[0])/2))):		# X < myX	sx
					quads[2]=1

			if quads[3]!=1:
				if m.last_emit[1]<my_pos[1] and (my_pos[0]-(abs((my_pos[1]-m.last_emit[1])/2)) <= m.last_emit[0] <= my_pos[0]-(abs((my_pos[1]-m.last_emit[1])/2))):		# Y < myY	giu
					quads[3]=1

		if quads==[1,1,1,1]:
			return False
		else:
			return True
		return False

	def evaluate_positions4(self, messages, my_pos):   # 1 messaggio solo  ## valuta se mandare in broadcast o no
		quads = [0,0,0,0]			# flags dei quadranti: 0 quadrante inesplorato, 1 quadrante esplorato
									# abbiamo scelto quadranti divisi da una X dalla nostra posizione

		for m in messages:
			dx = m.last_emit[0] - my_pos[0]
			dy = m.last_emit[1] - my_pos[1]
			#print("pos", my_pos[0], my_pos[1])
			#print("emit", m.last_emit[0], m.last_emit[1])
			#print("d", dx,dy)
			if dx >= 0 and dy >= 0:
				quads[0] = 1
			if dx >= 0 and dy  < 0:
				quads[1] = 1
			if dx  < 0 and dy >= 0:
				quads[2] = 1
			if dx  < 0 and dy  < 0:
				quads[3] = 1

		return quads!=[1,1,1,1]


	def evaluate_positions2(self, messages, my_pos):   # 1 messaggio solo  ## valuta se mandare in broadcast o no

		neighbor_positions = []   #positions of neighbors cars
		for c, i in zip(self.adj, range(len(self.adj))):
			if c == 1:
				#Ho preso la macchina corrispondente
				obj = self.sim.getCar(i)
				if obj != None:
					neighbor_positions.append(obj.pos)


		for m in messages:
			for emit in m.emitters:  #per ogni emitter diversa che ha mandato il messaggio
				if not in_range(my_pos, emit, 2*self.sim.rmin):  #se un emitter è troppo distante da me la scarto
					continue
				for neighbor_pos in list(neighbor_positions):  #controllo se un mio vicino ha già ricevuto un messaggio da un emitter precedente
					if in_range(neighbor_pos, emit, self.sim.rmin):
						neighbor_positions.remove(neighbor_pos)

		return len(neighbor_positions) > 0   #ritorno true se ci sono ancora dei vicini non coperti da nessun emitter precedente


	def evaluate_positions3(self, messages, my_pos):
		#ritrasmetti il messaggio con una certa probabilità P
		P = 0.95
		return random.random() > (1-P)




from simulator import Simulator  #se lo metto sopra si sfascia (cyclic imports), todo soluzione migliore
