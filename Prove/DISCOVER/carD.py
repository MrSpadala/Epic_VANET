import random
from time import sleep
from decimal import Decimal
from collections import deque
from pdb import set_trace
from math import sqrt
from packetsD import *
from enum import Enum
from visualGraph import *
from threading import Timer



class State(Enum):
	VULNERABLE = 0
	INFECTED = 1
	RECOVERED = 2


def dist(p,q):
	return sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)
def in_range(p, q, radius):  #ritorna se p e q sono distanti meno di 'radius'
	return dist(p,q) < radius


class Car:
	#Costruttore
	def __init__(self, plate, pos, adj):
		self.plate = plate
		self.pos = pos
		self.requests = []
		self.state = State.VULNERABLE
		self.timer_infected = None
		self.adj = adj
		self.sim = None  #simulator object
		self.req = None
		self.dis = 0

	def modifyMsg(self, req):
		#Modifico il messaggio con i miei dati
		req.Vtx = req.Vrx
		req.Vrx = self
		#req.NRP = RMIN+req.Vtx.pos
		req.pos = self.pos
		req.hlc-=1
		self.req = req



	def broadMsg(self):
		bcast = self.RN_election()
		if (not bcast):
			return
		#manca il controllo delle direzioni

		req = self.req.cloneReq()
		self.modifyMsg(req)

		#Se il messaggio è arrivato al limite di hop mi fermo
		if req.hlc == 0:
			return

		#Simulo la perdita di una percentuale di messaggi
		if random.random() < Simulator.DROP:
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
				obj.infect(req)

		if not self.sim.no_graphics:
			sleep(0.01)

		self.requests.clear()


	def infect(self, req):
		self.sim.rcv_messages += 1
		#se e' il primo messaggio faccio partire il timer di attesa
		#altrimenti aggiungo solo il messaggio alla lista
		if self.state == State.RECOVERED:   #Se è RECOVERED nessuna infezione ha effetto
			return

		if self.state == State.VULNERABLE:  #Se la macchina ancora non è infettata allora viene infettata e settato il timer
			self.sim.t_last_infected = self.sim.t
			self.sim.n_hop_last_infected = req.hl - req.hlc
			self.req = req
			self.state = State.INFECTED
			self.timer_infected = self.getWaitingTime(req.Vtx.pos)   #setta il timer di attesa in funzione della distanza dell'emitter
			#decomment to see all timers
			#print("timer_infected set to:", self.timer_infected * Simulator.TIME_RESOLUTION, "seconds")



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




	#####################################################PROTOCOL###############################################


	# messaggio.Vector è una list di tuple ( veicolo , veicolo.dist )

	def sortSecond(self, val):
	    return val[1]

	def bkRoutine(self, bool):
		if len(self.requests)>0:
			bool = False
		else:
			bool = True


	def setBkTimer(self, value):
		# settiamo un timer di valore value
		t = Timer(value, self.bkRoutine, (bool,))
		t.start()

		return bool
		# chiamiamo la backup routine (booooh)

	def RN_election(self):
		self.req.Vrx.dis = dist(self.req.Vrx.pos,self.req.Vtx.pos) - Simulator.RMIN
		self.req.Vector.append((self.req.Vrx, self.req.Vrx.dis))

		##########preso dal nostro evaluate position##############
		neighborhood = []   #positions of neighbors cars
		for c, i in zip(self.req.Vrx.adj, range(len(self.req.Vrx.adj))):
			if c == 1:
				#Ho preso la macchina corrispondente
				obj = self.req.Vrx.sim.getCar(i)
				if obj != None:
					neighborhood.append(obj)
		##########################################################


		for v in neighborhood:
			dis = dist(v.pos, self.req.Vtx.pos) - Simulator.RMIN
			self.req.Vector.append((v, dis))
		self.req.Vector.sort(key=self.sortSecond)	# sort in base a dist
		if self.req.Vector[0]==self.req.Vrx:
			return True		# a questo punto broadcastiamo
		else:
			return self.setBkTimer(self.req.Td*find(self.req.Vector, self.req.Vrx))	#torna sempre True, mannaggia la pupazza



#########################################################################################################

def find(lista, obj):
	i=0
	for o in lista:
		if o[0]==obj:
			return i
		else:
			i+=1




from discoverSimulator import Simulator  #se lo metto sopra si sfascia (cyclic imports), todo soluzione migliore
