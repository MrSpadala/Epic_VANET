
import random
from car import State as carState


random.seed(42)

class Simulator:

	MAX_STEP = 100000  #high as needed
	TIME_RESOLUTION = 0.1  #0.1 seconds per iteration

	# Environment parameters
	TMAX = 3		#tempo di attesa massima prima di mandare un messaggio in broadcast, in secondi
	TMIN = 0.3		#tempo di attesa minima prima di mandare un messaggio in broadcast, in secondi
	R = 80			#raggio massimo di comunicazione
	ALPHA = 0.8		#quanto tempo di attesa deve essere deterministico e quanto non deterministico.
					#ALPHA in [0,1]. ALPHA=1 è completamente deterministico, ALPHA=0 non deterministico.
					# (possiamo aggiungere dopo che ALPHA non è costante ma magari dipende da macchina a macchina, a seconda delle condizioni del traffico)

	def init(self):
		self.cars = []

		# TODO: populate cars and add vpython code

		# Create a dictionary plate-->car-object
		self.car_dict = {c.plate: c for c in self.cars}


	def runSimulation():
		for t in range(MAX_STEP):
			for car in cars:
				if car.state == carState.INFECTED:
					car.timer_infected -= 1
					
					if car.timer_infected <= 0:
						car.timer_infected = None
						car.state == carState.RECOVERED
						car.broadMsg()

	@staticmethod
	def getCar(plate):
		return car_dict[plate]

