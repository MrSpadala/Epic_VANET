
import abc
import math
import simulator

class _Event:
	"""
	Abstract representation of a simulation event, which is scheduled and executed by the simulator
	"""

	def __init__(self, t):
		self.delay = math.ceil(t)  # simulator time to wait before scheduling the event

	def __lt__(self, event):
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
		for c, i in zip(self.vehicle.adj, range(len(self.vehicle.adj))):
			if c == 1:
				neighbor = sim.getCar(i)  #take the car object
				if neighbor == None:
					continue		

				# If needed update GUI
				if not sim.no_graphics:
					if neighbor.state == State.VULNERABLE:
						visualInfect(self.vechicle, neighbor)

				neighbor.on_receive(self.msg)  #TODO: don't infect immediately, wait some time theta

		# If using GUI sleep a bit
		if not sim.no_graphics:
			sleep(0.01)




if __name__ == "__main__":
	import sys
	sys.path.append("./src/")


	


