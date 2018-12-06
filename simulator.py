
import random
import functools
from collections import defaultdict
from car import Car, State as carState
from msg import Msg
from pdb import set_trace as breakpoint
from visualGraph import *

random.seed(42)

class Simulator:

	# Simulation parameters
	SECONDS_SIM = 120  #high as needed
	TIME_RESOLUTION = 0.1  #0.1 seconds per iteration

	# Environment parameters
	TMAX = 3		#tempo di attesa massima prima di mandare un messaggio in broadcast, in secondi
	TMIN = 0.4		#tempo di attesa minima prima di mandare un messaggio in broadcast, in secondi
	R = 300			#raggio massimo di comunicazione
	ALPHA = 0.8		#quanto tempo di attesa deve essere deterministico e quanto non deterministico.
					#ALPHA in [0,1]. ALPHA=1 è completamente deterministico, ALPHA=0 non deterministico.
					# (possiamo aggiungere dopo che ALPHA non è costante ma magari dipende da macchina a macchina, a seconda delle condizioni del traffico)

	# Metrics variables
	rcv_messages = 0  #number of received messages
	sent_messages = 0 #number of sent messages

	def __init__(self, cars):
		self.cars = cars
		for car in self.cars:
			car.sim = self

		# Create a dictionary plate-->car-object
		#_car_dict = {c.plate: c for c in self.cars}
		_car_dict = {c.plate: c for c in self.cars if c != None}
		self.car_dict = defaultdict(lambda: None, _car_dict)



	def runSimulation(self):
		for t in range(int(Simulator.SECONDS_SIM/Simulator.TIME_RESOLUTION)):
			for car in cars:	# k è la chiave dell'elemento
				if car.state == carState.INFECTED:
					car.timer_infected -= 1

					if car.timer_infected <= 0:
						car.timer_infected = None
						car.state = carState.RECOVERED
						car.broadMsg()

	def getCar(self, plate):
		return self.car_dict[plate]



def init():
	positions = []
	p = open("grafi/Luxembourg/pos/pos_time27100Tper50.txt", "r")
	for i in p:
		d = i.split(' ')
		if d[2] == '27100':  #riga fallata
			positions.append(None)
		else:		
			positions.append((float(d[2]), float(d[3])))
			#sphere(pos=vector(float(d[2]),float(d[3]),0), radius=20)


	a = open("grafi/Luxembourg/adj/adj_time27100Tper50.txt", "r")
	adi = []
	for l in a:
		adi.append([int(n) for n in l.split(' ')])   #get the value as an int
	#breakpoint()
	cars = [Car(i,p,a) if p else None for i,p,a in zip(range(len(adi)),positions,adi)]   #Use as plate the index of the car
	cars = list(filter(lambda x: x != None, cars))
	return cars


if __name__ == "__main__":
	cars = init()
	s = Simulator(cars)
	bubbles = displayCars(s.car_dict)
	#random.sample(cars, 1)[0].infect(Msg.dummy())
	firstinfected = s.getCar(firstInfection())
	firstinfected.infect(Msg(firstinfected.plate, 'ciao', (firstinfected.pos[0], firstinfected.pos[1]), (firstinfected.pos[0], firstinfected.pos[1]), 0, 100))
	s.runSimulation()
	#for c,i in zip(cars,range(len(cars))):
	#	print(i, c.state)
	tmp = str([c.state if c else None for c in cars])
	print()
	print("Simulation ended")
	print("Vulnerable: ", tmp.count("State.VULNERABLE"))
	print("Infected: ", tmp.count("State.INFECTED"))
	print("Recovered: ", tmp.count("State.RECOVERED"))
	print()
	print("Metrics")
	print("#sent messages: ", s.sent_messages)
	print("#received messages: ", s.rcv_messages)
