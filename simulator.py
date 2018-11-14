
from car import State as carState



class Simulator:

	MAX_T = 100000
	TIME_RESOLUTION = 0.1  #0.1 seconds per iteration

	def init(self):
		self.cars = []
		# TODO: populate cars

		# Create a dictionary plate-->car-object
		self.car_dict = {c.plate: c for c in self.cars}


	def runSimulation():
		for t in range(MAX_T):
			for car in cars:
				if car.state == carState.INFECTED:
					car.timer_infected -= 1
					
					if car.timer_infected == 0:
						car.timer_infected = None
						car.state == carState.RECOVERED
						car.broadMsg()

	@staticmethod
	def getCar(plate):
		return car_dict[plate]

