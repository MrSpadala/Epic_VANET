
import abc
import math
import time

import simulator
import car
import visualGraph

class _Event:
	"""
	Abstract representation of a simulation event, which is scheduled and executed by the simulator
	"""

	def __init__(self, t):
		"""simulation time to wait before scheduling the event"""
		self.delay = math.ceil(t)

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
	TX_DELAY = 2    # transmission delay, expressed in ms

	def __init__(self, vehicle_src, msg):
		delay = (self.TX_DELAY / 1000) / simulator.Simulator.TIME_RESOLUTION
		super().__init__(delay)
		self.vehicle = vehicle_src
		self.msg = msg

	def execute(self, sim):
		"""
		Send the message to all 'vehicle''s neighbors
		"""
		for i in self.vehicle.neighbors:
			neighbor = sim.getCar(i)  #take the car object
			if neighbor == None:
				raise "IS NONEEEE in events"
				continue		

			# If needed update GUI
			if not sim.no_graphics:
				if neighbor.state == car.State.VULNERABLE:
					visualGraph.visualInfect(self.vehicle, neighbor)

			neighbor.on_receive(self.msg)

		# If using GUI sleep a bit
		if not sim.no_graphics:
			time.sleep(0.01)




	


