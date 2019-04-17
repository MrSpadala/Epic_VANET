
import os
import sys
import pickle
import random
import functools
from math import sqrt
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

random.seed(42)

class Simulator:

	# Simulator parameters
	TIME_RESOLUTION = 0.01  #how many seconds per step

	# Environment parameters
	TMAX = 0.9		#max time to wait before sending a broadcast message
	TMIN = 0		#min time to wait before sending a broadcast message
	RMIN = 170		#Rmin, expressed in meters
	RMAX = 500		#Rmax, expressed in meters
	DROP = 0.03		#message drop rate
	ALPHA = 0.05    #if at the end of the waiting timer, a fraction larger than ALPHA
					#of my neighors has not been reached I relay the message

	def __init__(self, cars):
		self.cars = cars
		for car in self.cars:
			car.sim = self

		self.rmin = Simulator.RMIN

		# Create a dictionary plate-->car-object
		#_car_dict = {c.plate: c for c in self.cars}
		_car_dict = {c.plate: c for c in self.cars if c != None}
		self.car_dict = defaultdict(_ret_none, _car_dict)

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
		if not self.no_graphics:
			print('GUI mode, to disable it run with \'--no-graphics\'')



	def runSimulation(self):
		# Set counter for infected cats
		cars_inftd = [c.state == carState.INFECTED for c in self.cars]   #cars infected at the start of the simulation
		self.infected_counter = sum(cars_inftd)
		# Set simulation tick  
		self.t = 0

		#print('started sim with inf counter', self.infected_counter)
		while self.infected_counter > 0:
			self.t += 1
			for car in self.cars:
				if car.state == carState.INFECTED:
					car.timer_infected -= 1

					if car.timer_infected <= 0:
						car.timer_infected = None
						car.transition_to_state(carState.RECOVERED)
						car.broadMsg()

	def getCar(self, plate):
		return self.car_dict[plate]



def init_cars():
	city_name, scenario = "Luxembourg", "time27100Tper1000.txt"   #USE LUXEMBURG
	#city_name, scenario = "Cologne", "time23000Tper1000.txt"     #USE COLOGNE
	#return init_cars_newyork()									  #USE NEWYORK
	
	fpath = os.path.join("cached", city_name+"_"+scenario+'.bin')
	cached = _load_cached(fpath)
	if cached:	return cached

	print('Computing car graph...')
	positions = []
	p = open("grafi/"+city_name+"/pos/pos_"+scenario, "r")
	for i in p:
		d = i[:-1].split(' ')  #discard trailing \n
		if d[0] == d[2] and d[2] == d[4]:  #don't append malformed rows
			positions.append(None)
		else:
			positions.append((float(d[2]), float(d[3])))

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

def _ret_none():
	return None




#Perform a single simulation
def performSimulation(i, verbose=True):
	cars = init_cars()

	def print_graph_stats():
		grade = 0
		for car in cars:
			for a in car.adj:
				grade += a
		print('number of cars', len(cars))
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

	if verbose:
		tmp = str([c.state for c in cars])
		print("Simulation", i, "ended")
		print("Vulnerable: ", tmp.count("State.VULNERABLE"))
		print("Infected: ", tmp.count("State.INFECTED"))
		print("Recovered: ", tmp.count("State.RECOVERED"))
		print()

	return s




#Performs 'n' different simulations
def performSimulations(n):

	print('[+] Caching cars data')
	init_cars()  #trick to cache the car graph before starting the simulation
	print('[+] Done!')

	if n > 1:
		cpus = 4
		with Pool(cpus) as pool:
			print('[+] Starting', n, 'simulations with', cpus, 'parallel jobs')
			sims = pool.map(performSimulation, range(n))
	else:
		sims = [ performSimulation(0) ]
	

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
	std_dev = 0
	for s in sims:
		std_dev += (str([c.state for c in s.cars]).count("State.RECOVERED")) ** 2
	std_dev = (std_dev / len(sims))  -  ((infected/len(sims))**2)
	std_dev = sqrt(std_dev)
	print("Cars infected std dev: {:.2f}".format(std_dev))


	return (Simulator.RMIN, #for boxplots
		[s.sent_messages for s in sims],
		[str([c.state for c in s.cars]).count("State.RECOVERED") for s in sims],
		[s.t_last_infected for s in sims],
		[s.n_hop_last_infected for s in sims])


if __name__ == "__main__":
	if "--no-graphics" in sys.argv:
		performSimulations(400)
	else:
		performSimulations(1)
