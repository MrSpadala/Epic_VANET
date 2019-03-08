
import os
import sys
import pickle
import random
import functools
from multiprocessing import Pool
from collections import defaultdict
from car import Car, State as carState
from msg import Msg
from grafi.DFS import get_largest_conn_component
from pdb import set_trace as breakpoint
from visualGraph import *

try:
	from tqdm import tqdm
except:
	tqdm = lambda x: x

random.seed(320)

class Simulator:

	# Simulation parameters
	SECONDS_SIM = 10  #TODO change and iterate while there are infected cars
	TIME_RESOLUTION = 0.01 #how many seconds per iteration

	# Environment parameters
	TMAX = 0.9		#tempo di attesa massima prima di mandare un messaggio in broadcast, in secondi
	TMIN = 0		#tempo di attesa minima prima di mandare un messaggio in broadcast, in secondi
	RMIN = 250		#raggio minimo di comunicazione, espresso in metri
	RMAX = 500		#raggio massimo di comunicazione, espresso in metri
	DROP = 0.03		#rate di messaggi persi spontaneamente nella trasmissione
	#ALPHA = 1		#quanto tempo di attesa deve essere deterministico e quanto non deterministico.
					#ALPHA in [0,1]. ALPHA=1 è completamente deterministico, ALPHA=0 non deterministico.
					# (possiamo aggiungere dopo che ALPHA non è costante ma magari dipende da macchina a macchina, a seconda delle condizioni del traffico)

	def __init__(self, cars):
		self.cars = cars
		for car in self.cars:
			car.sim = self

		self.rmin = Simulator.RMIN

		# Create a dictionary plate-->car-object
		#_car_dict = {c.plate: c for c in self.cars}
		_car_dict = {c.plate: c for c in self.cars if c != None}
		self.car_dict = defaultdict(lambda: None, _car_dict)
		
		def print_density():
			cars, edges = 0, 0
			for k,car in self.car_dict.items():
				cars += 1
				for a in car.adj:
					edges += 1 if (a==1 and self.car_dict[a]!=None) else 0
			print('number of cars', cars)
			print('number of edges', edges/2)
			print('density', edges/(2*cars))

		#print_density()

		# Simulation variables
		self.t = 0   #current simulation iteration
		self.infected_counter = 0	 #keep track of cars currently in INFECTED state

		# Metrics variables
		self.rcv_messages = 0  #number of received messages
		self.sent_messages = 0 #number of sent messages
		self.t_last_infected = 0  #time step of the last car infected
		self.n_hop_last_infected = 0  #number of hops of last infected car

		# Args
		self.no_graphics = "--no-graphics" in sys.argv



	def runSimulation(self):
		# Set counter for infected cats
		cars_inftd = [c.state == carState.INFECTED for c in self.cars]   #cars infected at the start of the simulation
		self.infected_counter = sum(cars_inftd)
		# Set simulation tick  
		self.t = 0

		#print('started sim with inf counter', self.infected_counter)
		while self.infected_counter > 0:
			self.t += 1
			for car in self.cars:	# k è la chiave dell'elemento
				if car.state == carState.INFECTED:
					car.timer_infected -= 1

					if car.timer_infected <= 0:
						car.timer_infected = None
						car.transition_to_state(carState.RECOVERED)
						car.broadMsg()

	def getCar(self, plate):
		return self.car_dict[plate]



def init_cars():
	city_name, scenario = "Luxembourg", "time27100Tper1000.txt"
	#city_name, scenario = "Cologne", "time23000Tper1000.txt"
	
	fpath = os.path.join("cached", city_name+"_"+scenario+'.bin')
	cached = _load_cached(fpath)
	if cached:	return cached

	print('Computing car graph...')
	positions = []
	p = open("grafi/"+city_name+"/pos/pos_"+scenario, "r")
	for i in p:
		d = i[:-1].split(' ')  #discard trailing \n
		if d[0] == d[2] and d[2] == d[4]:  #riga fallata
			positions.append(None)
		else:
			positions.append((float(d[2]), float(d[3])))
			#sphere(pos=vector(float(d[2]),float(d[3]),0), radius=20)


	a = open("grafi/"+city_name+"/adj/adj_"+scenario, "r")
	adi = []
	for l in a:
		adi.append([int(n) for n in l.split(' ')])   #get the value as an int
	cars = [Car(i,p,a) if p else None for i,p,a in zip(range(len(adi)),positions,adi)]   #Use as plate the index of the car
	cars = list(filter(lambda x: x != None, cars))
	cars = get_largest_conn_component(cars)
	pickle.dump(cars, open(fpath, 'wb'))
	return cars

def init_cars_newyork():
	fname = 'Newyork5003.mat'
	fpath = os.path.join("cached", fname+'.bin')
	cached = _load_cached(fpath)
	if cached:	return cached

	print('Computing car graph...')
	import scipy.io as sio
	import numpy as np
	contents = sio.loadmat(os.path.join('grafi/NewYork/', fname))
	adia, coord = contents['Adia'], contents['coord']
	coord = [(x,y) for x,y in zip(coord[0], coord[1])]
	cars = []
	for i,c,a in zip(range(len(adia)),coord,adia):
		cars.append(Car(i,c,a))
	cars = get_largest_conn_component(cars)
	pickle.dump(cars, open(fpath, 'wb'))
	return cars


def _load_cached(fpath):
	if not os.path.exists("cached"):
		os.makedirs("cached")
	if os.path.exists(fpath):
		return pickle.load(open(fpath, "rb"))
	return None


#Performs 'n' different simulations
def performSimulations(n, with_outliers=False):

	#Perform a single simulation
	def performSimulation():
		cars = init_cars_newyork()

		def print_graph_stats():
			grade = 0
			for car in cars:
				for a in car.adj:
					grade += a
			print('number of edges', grade/2)
			print('density', grade/(2*len(cars)))

		#print_graph_stats()

		s = Simulator(cars)

		if s.no_graphics:
			random.sample(cars, 1)[0].infect(Msg.dummy())
		else:
			bubbles = displayCars(s.car_dict)
			firstinfected = s.getCar(firstInfection())
			firstinfected.infect(Msg(firstinfected.plate, 'ciao', (firstinfected.pos[0], firstinfected.pos[1]), (firstinfected.pos[0], firstinfected.pos[1]), 0, 100))

		s.runSimulation()
		tmp = str([c.state for c in cars])
		print("Simulation ended")
		print("Vulnerable: ", tmp.count("State.VULNERABLE"))
		print("Infected: ", tmp.count("State.INFECTED"))
		print("Recovered: ", tmp.count("State.RECOVERED"))
		print()

		# Return Simulator or, if the simulation was too bad, don't return it
		if with_outliers:
			return s
		return s if tmp.count("State.RECOVERED")>0.05*len(cars) else None  #consider as outlier a simulation where less than 5% of the cars got infected


	sims = [performSimulation() for i in tqdm(range(n))]  #list with Simulator objects
	sims = list(filter(lambda x: x!=None, sims))    #filter out None

	print()
	print("Average metrics with rmin =",Simulator.RMIN)
	print("#sent messages: ", sum([s.sent_messages for s in sims])/n)
	print("#received messages: ", sum([s.rcv_messages for s in sims])/n)
	print("time of last car infection: ", sum([s.t_last_infected for s in sims])*Simulator.TIME_RESOLUTION/n)
	print("#hops to reach last infected car: ",sum([s.n_hop_last_infected for s in sims])/n)
	infected = 0
	for s in sims:
		infected += str([c.state for c in s.cars]).count("State.RECOVERED")
	print("Cars infected ratio: {:.2f}%".format(100*(infected) / (len(sims)*len(sims[0].cars))))

	return (Simulator.RMIN, #for boxplots
		[s.sent_messages for s in sims],
		[str([c.state for c in s.cars]).count("State.RECOVERED") for s in sims],
		[s.t_last_infected for s in sims],
		[s.n_hop_last_infected for s in sims])
	#return (Simulator.RMIN,  #for graphs
	#	sum([s.sent_messages for s in sims])/n,
	#	100*(infected+15) / (len(sims)*len(sims[0].cars)))



def do_tests(r):
	Simulator.RMIN = r
	return performSimulations(10, with_outliers=True)


if __name__ == "__main__":
	if "--no-graphics" in sys.argv:
		#with Pool(4) as pool:
			#print( pool.map(do_tests, range(50, 341, 10)) )
		do_tests(550)

	else:
		performSimulations(1)
