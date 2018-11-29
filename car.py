import random
from math import sqrt
from msg import Msg
from enum import Enum


class State(Enum):
	VULNERABLE = 0
	INFECTED = 1
	RECOVERED = 2


def dist(p,q):
	return sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)
	

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
	
	def modifyMsg(self, msg):
		#Modifico il messaggio con i miei dati
		msg.emit = self.pos
		msg.hop += 1
	
	def broadMsg(self):
		msg = self.messages[0]  #prendo il primo messaggio della lista, quello che ha generato l'infezione
		self.modifyMsg(msg)
		#Se il messaggio è arrivato al limite di hop mi fermo
		if msg.hop == msg.ttl:
			return
		
		if (not self.evaluate_positions(self.messages, self.pos)):
			return
		#manca il controllo delle direzioni
		
		for c, i in zip(self.adj, range(len(self.adj))):
			if c == 1:
				#Ho preso la macchina corrispondente
				obj = self.sim.getCar(i)
				obj.infect(msg)

		self.messages.clear()				
		

	def infect(self, msg):
		#se e' il primo messaggio faccio partire il timer di attesa
		#altrimenti aggiungo solo il messaggio alla lista
		if self.state == State.RECOVERED:   #Se è RECOVERED nessuna infezione ha effetto
			return

		if self.state == State.VULNERABLE:  #Se la macchina ancora non è infettata allora viene infettata e settato il timer
			self.state = State.INFECTED
			self.timer_infected = self.getWaitingTime(msg.emit)   #setta il timer di attesa in funzione della distanza dell'emitter

		self.messages.append(msg)


	def getWaitingTime(self, emit_pos):
		#print(self.pos, emit_pos)
		dAS = dist(self.pos, emit_pos)   #distanza tra me e l'emittente che me lo ha mandato, espressa in metri
		t_dist = Simulator.TMAX*(1 - dAS/Simulator.R)   #tempo di attesa dipendente dalla distanza, espresso in secondi
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
					
		#print("Decidendo...")

		if quads==[1,1,1,1]:
			return False
		else:
			return True


from simulator import Simulator  #se lo metto sopra si sfascia (cyclic imports), todo soluzione migliore
