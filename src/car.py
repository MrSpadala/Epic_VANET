
import random
import math
from enum import Enum

import Events
import simulator
from msg import Msg
from visualGraph import *



class State(Enum):
	VULNERABLE = 0
	INFECTED = 1
	RECOVERED = 2


# TODO: transform the representation of the connectivity graph, from adjacency matrix to list of neighbors

# TODO: dist and in_range are the critical part of the program (most of the time spent inside them).
#       Should precompute, for the current value of RMIN, the which car is in range of which other car,
#       Maybe saving in each Car object the (plates of) other cars at distance <= RMIN

def dist(p,q):  #eucledian distance
	return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)
def in_range(p,q,radius):	#returns true whether the distance p,q is less than radius
	return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2) < radius


class Car:

	def __init__(self, plate, pos, neighbors):
		self.plate = plate          #identifier of the car
		self.pos = pos              #tuple (x,y)
		self.neighbors = neighbors  #list of plates of neighbor cars

		# Simulation attributes
		self.messages = []   #messages received during the waiting phase
		self.state = State.VULNERABLE    #state of the vehicle w.r.t. the disseminated message
		self.sim = None   # Each car keeps track of its own simulator object, which is set right before starting the simulation


	def on_receive(self, msg):
		"""
		Implements the receiving of a message
		"""
		#Simulate message loss while receiving
		if random.random() < simulator.Simulator.DROP:
			return

		self.sim.rcv_messages += 1   #for simulation statistics

		# If I already received this message (RECOVERED state) I don't do anything
		if self.state == State.RECOVERED:
			return

		if self.state == State.VULNERABLE:
			# If it's the first time that I receive the message, then transition to state infected and update simulation stats
			self.sim.t_last_infected = self.sim.t
			self.sim.t_infected[self.sim.t] += 1
			self.sim.infected_counter += 1
			self.state = State.INFECTED

			# Add waiting phase event
			waiting_time = self.getWaitingTime(msg.last_emit)
			event = Events.WaitingEvent(self, waiting_time)
			self.sim.schedule_event(event)

		# Store the received message
		self.messages.append(msg)


	def getWaitingTime(self, emit_pos):
		"""
		Returns the waiting time a vehicle has to wait when infected.
		Calculated using the distance between me and the emitter that sent 
		me the message, expressed as number of simulator ticks
		"""
		Simulator = simulator.Simulator

		dAS = dist(self.pos, emit_pos) 
		waiting_time = Simulator.TMAX*(1 - dAS/Simulator.RMAX)  #waiting time, in seconds

		if waiting_time <= Simulator.TMIN:
			waiting_time = Simulator.TMIN
		if waiting_time >= Simulator.TMAX:
			waiting_time = Simulator.TMAX

		# Converts from seconds to simulator ticks
		return waiting_time / Simulator.TIME_RESOLUTION



	def broadcast_phase(self):
		"""
		After the waiting phase, a vehicle has to decide whether or not to relay the received message.
		Here we perform the decision process and, if positive, we send the message to all our radio neighbors (infect)
		"""

		# Decide whether to relay or not
		bcast = self.evaluate_positions(self.messages, self.pos)
		
		if bcast:
			# Take the first message in the list of incoming messages (the first message generated the infection)
			# and modify it to be ready for broadcast
			msg_recv = self.messages[0]
			msg = self.modify_msg(msg_recv)

			# Don't broadcast if the message reached its hop limit
			if msg.hop == msg.ttl:
				return

			# Update simulator statistics
			self.sim.sent_messages += 1
			self.sim.network_traffic += msg.size()   #EPIC
			#self.sim.network_traffic += len(msg.text)  #probabilistic

			# Send the message by scheduling an event for the simulator (this implements some network delay)
			#self.send_msg_to_neighbors(msg)
			bcast_event = Events.BroadcastEvent(self, msg)
			self.sim.schedule_event(bcast_event)

		# Change state to recovered and update simulation statistics, either the vehicle has broadcasted or not
		self.messages.clear()
		self.sim.infected_counter -= 1
		self.state = State.RECOVERED


	def modify_msg(self, _msg):
		"""
		Before a vehicle retransmit a message, this last one must be modified by
		adding data of the vehicle which is about to broadcast it. It returns a new Msg object, no side effects
		"""

		msg = _msg.clone()
		
		# Update 'msg''s last emitter with this vehicle position
		msg.last_emit = self.pos

		# Update hop counter
		msg.hop += 1

		# Retrieve the set of all known emitters. It is the union of all emitters inside all messages
		# received during the sleep time.
		all_emitters = set([self.pos])
		for m in self.messages:
			all_emitters = all_emitters.union(m.emitters)
		
		# Sort the emitters list by the distance between them and this vehicle, in ascending order
		key = lambda x: dist(x, self.pos)
		all_emitters_srtd = sorted(list(all_emitters), key=key)
		# Keep only the closest to me, since there is Msg.EMITTERS_LIMIT limit on the max. number of emitters stored inside a message
		msg.emitters = all_emitters_srtd[:Msg.EMITTERS_LIMIT]

		return msg
		



	# Now a barrage of different 'evaluate_positions' functions, that decide whether
	# or not a vehicle has to relay a message. Each function follows its own policy


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
		return len(neighbor_positions) > simulator.Simulator.ALPHA * n_neighbors


	# WE USED THIS as algorithm comparison
	def evaluate_positions_no_geo(self, messages, my_pos):
		return not len(messages)>3

	# WE USED THIS as algorithm comparison
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


