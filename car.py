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


def dist(p,q):  #eucledian distance
	return sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)
def in_range(p,q,radius):	#returns true whether the distance p,q is less than radiu
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
		#Update the message with my data
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
		bcast = self.evaluate_positions_probabilistic(self.messages, self.pos)
		if (not bcast):
			return

		#take the first message in the list of incoming messages (the first message generated the infection)
		msg = self.messages[0].clone()
		self.modifyMsg(msg, self.messages)

		#Don't broadcast if the message reached its hop limit
		if msg.hop == msg.ttl:
			return

		#Update simulator statistics
		self.sim.sent_messages += 1
		self.sim.network_traffic += msg.size()   #EPIC
		#self.sim.network_traffic += len(msg.text)  #probabilistic

		#Send message to all my neighbors
		for c, i in zip(self.adj, range(len(self.adj))):
			if c == 1:
				obj = self.sim.getCar(i)  #take the car object
				if obj == None:
					continue					

				if not self.sim.no_graphics:
					if obj.state == State.VULNERABLE:
						visualInfect(self, obj)
				obj.infect(msg)

		if not self.sim.no_graphics:
			sleep(0.01)

		self.messages.clear()



	def infect(self, msg):
		#Simulate message loss while receiving
		if random.random() < Simulator.DROP:
			return

		self.sim.rcv_messages += 1   #for simulation statistics

		# If I already received this message (RECOVERED state) I don't do anything
		if self.state == State.RECOVERED:
			return

		# If it's the first time that the message arrive, I go from VULNERABLE state to
		# INFECTED state, then I start the waiting timer
		if self.state == State.VULNERABLE:
			self.sim.t_last_infected = self.sim.t
			self.sim.n_hop_last_infected = msg.hop
			self.transition_to_state(State.INFECTED)
			self.timer_infected = self.getWaitingTime(msg.last_emit)  #set waiting timer in function of the distance 

		self.messages.append(msg)



	def getWaitingTime(self, emit_pos):
		""" Returns the waiting time a vehicle has to wait when infected.
		Calculated using the distance between me and the emitter that sent 
		me the message, expressed as number of simulator ticks
		"""
		dAS = dist(self.pos, emit_pos) 
		waiting_time = Simulator.TMAX*(1 - dAS/Simulator.RMAX)  #waiting time, in seconds

		if waiting_time <= Simulator.TMIN:
			waiting_time = Simulator.TMIN
		if waiting_time >= Simulator.TMAX:
			waiting_time = Simulator.TMAX

		# Converts from seconds to simulator ticks
		return waiting_time / Simulator.TIME_RESOLUTION



	# WE USED THIS
	def evaluate_positions(self, messages, my_pos):   # 1 messaggio solo  ## valuta se mandare in broadcast o no

		neighbor_positions = []   #positions of neighbors cars
		for c, i in zip(self.adj, range(len(self.adj))):
			if c == 1:
				#Ho preso la macchina corrispondente
				obj = self.sim.getCar(i)
				if obj != None:
					neighbor_positions.append(obj.pos)

		n_neighbors = len(neighbor_positions)

		for m in messages:
			for emit in m.emitters:  #per ogni emitter diversa che ha mandato il messaggio
				for neighbor_pos in list(neighbor_positions):  #controllo se un mio vicino ha già ricevuto un messaggio da un emitter precedente
					if in_range(neighbor_pos, emit, self.sim.rmin):
						neighbor_positions.remove(neighbor_pos)
		
		# return true (relay) only if there is a percentage ALPHA of uncoverd neighbors
		return len(neighbor_positions) > Simulator.ALPHA * n_neighbors



	def evaluate_positions_no_geo(self, messages, my_pos):
		return not len(messages)>3

	def evaluate_positions_w_p_pers(self, messages, my_pos):
		P = []
		for m in messages:
			d = dist(m.last_emit, my_pos)
			Rmean = (Simulator.RMIN/4) / 2
			P.append(d/Rmean)
		return random.random() > (1-min(P))



	# WE USED THIS as the probabilistic dissemination
	def evaluate_positions_probabilistic(self, messages, my_pos):
		#relay the message with probability P
		'''bcast_force = True
		for m in messages:
			if dist(my_pos, m.last_emit) <= Simulator.RMIN:
				bcast_force = False'''
		bcast_force = len(messages) > 1
		P = 0.6
		return bcast_force or random.random() > (1-P)

		#other prb relay (inv proportional to the distance from the closest relay)
		'''
		min_dist = Simulator.RMAX
		for m in messages:
			for emit in m.emitters:  #per ogni emitter diversa che ha mandato il messaggio
				d = dist(emit, self.pos)
				if d < min_dist:
					min_dist = d
		min_dist = min(min_dist, Simulator.RMAX)
		p = min_dist / Simulator.RMIN    #p is the relay probability
		return random.random() > (1-p)
		'''

		#other prb relay (inv prop with the number of neighbors)
		'''
		n_neighbors = 0   #number of neighbors cars
		for c, i in zip(self.adj, range(len(self.adj))):
			if c == 1:
				#Ho preso la macchina corrispondente
				obj = self.sim.getCar(i)
				if obj != None:
					n_neighbors += 1

		k = 45  #const
		if n_neighbors <= k:
			return True
		p = k/n_neighbors
		return random.random() > (1-p)
		'''


		


		

	# utility: transition a vehicle to a certain state
	def transition_to_state(self, state_final):
		if self.state == State.VULNERABLE and state_final == State.INFECTED:
			self.sim.infected_counter += 1
			self.state = State.INFECTED
		elif self.state == State.INFECTED and state_final == State.RECOVERED:
			self.sim.infected_counter -= 1
			self.state = State.RECOVERED
		else:
			raise ValueError('Inconsistent state transition from', self.state, 'to', state_final)



from simulator import Simulator  #se lo metto sopra si sfascia (cyclic imports), todo soluzione migliore
