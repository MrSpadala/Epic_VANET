
import abc
import math
import time
import random

import simulator
import car
import visualGraph
from sim_config import config

class _Event:
	"""
	Abstract representation of a simulation event, which is scheduled and executed by the simulator
	"""

	def __init__(self, t):
		"""simulation time to wait before scheduling the event"""
		self.delay = math.ceil(t / config.time_resolution)

	def __lt__(self, event):
		"""Look to Simulator.schedule_event for informations"""
		return True

	@abc.abstractmethod
	def execute(self, sim):
		pass



class WaitingEvent(_Event):
	"""
	Implements the waiting phase of a vehicle when it receives a message
	"""
	def __init__(self, vehicle, t):
		super().__init__(t)
		self.vehicle = vehicle
	
	def execute(self, sim):
		self.vehicle.broadcast_phase()





class BroadcastEvent(_Event):
	"""
	Implements a (constant) time delay from a message send to its reception by the receiver
	"""

	def __init__(self, vehicle_src, msg):
		# tx_delay is unif. distributed in tx_max and tx_min
		tx_min, tx_max = 0.5, 2.5  #expressed in ms
		tx_delay = random.random() * (tx_max-tx_min) + tx_min
		super().__init__(tx_delay / 1000)   #ms to s
		self.vehicle = vehicle_src
		self.msg = msg

	def execute(self, sim):
		"""
		Send the message to all 'vehicle''s neighbors
		"""
		for i in self.vehicle.neighbors:
			neighbor = sim.getCar(i)  #take the car object	

			# If needed update GUI
			if not sim.no_graphics:
				if neighbor.state == car.State.VULNERABLE:
					visualGraph.visualInfect(self.vehicle, neighbor)

			neighbor.on_receive(self.msg)

		# If using GUI sleep a bit
		if not sim.no_graphics:
			time.sleep(0.01)




	


