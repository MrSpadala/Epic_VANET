
import os
import sys
import heapq
import pickle
import random
from multiprocessing import Pool
from collections import defaultdict

import scipy.io as sio

import car
from graph_utils.DFS import get_largest_conn_component
from msg import Msg
from visualGraph import *



random.seed(42)


# Simulation parameters
N_CPUS = 1	   		   #how many cores to use
N_SIMULATIONS = 4    #how many simulations to perform

# TODO: move some configuration parameters in a separate config file


class Simulator:

	# Simulator parameters
	TIME_RESOLUTION = 0.0001  #how many seconds per step

	# Environment parameters
	TMAX = 0.3		#max time to wait before sending a broadcast message
	TMIN = 0		#min time to wait before sending a broadcast message
	RMIN = 170		#Rmin, expressed in meters
	RMAX = 500		#Rmax, expressed in meters
	DROP = 0.01		#message drop rate
	ALPHA = 0.05    #if at the end of the waiting timer, a fraction larger than ALPHA
					#of my neighors has not been reached I relay the message


	def __init__(self, cars):
		self.cars = cars

		# Register this 'Simulator' object to the vehicles
		for car in self.cars:
			car.sim = self

		self.rmin = Simulator.RMIN

		# Create a dictionary plate-->car-object
		_car_dict = {c.plate: c for c in self.cars if c != None}
		self.car_dict = defaultdict(_ret_none, _car_dict)

		# Simulation variables
		self.t = 0   #current simulation iteration
		self.infected_counter = 0	 #keep track of cars currently in INFECTED state
		self.events = []   #scheduled events (will be used as a heap through 'heapq' module)

		# Metrics variables
		self.rcv_messages = 0  #number of received messages
		self.sent_messages = 0 #number of sent messages
		self.t_last_infected = 0  #time step of the last car infected
		self.network_traffic = 0   #network traffic expressed in bytes
		self.t_infected = defaultdict(int)  #t_infected[t] = [...] list of cars infected at t

		# Args
		self.no_graphics = not "--with-graphics" in sys.argv


	def getCar(self, plate):
		"""
		Returns Car object given its identifier plate
		"""
		return self.car_dict[plate]



	def schedule_event(self, event):
		"""
		Pushes an event to the event queue. It will be executed
		at the current time of the simulation + the delay of the event. 
		e.g. if the event must be executed after 100 units of time after its
		creation (event.delay=100) and the current time of the simulation
		is 10000, then the event is executed at simulation time 10100.

		heapq.heappush will push to the heap the tuple (T, event), where
		T is the time when the event will be executed. The heap is ordered
		by T, so that when we fetch the next event we are taking the event
		with the smallest T. Event.__lt__ is defined to be always true, 
		since we care only that they are ordered by T
		"""
		heapq.heappush(self.events, (self.t+event.delay, event))


	def runSimulation(self):
		"""
		Loop that fetches and executes the most recent event
		"""
		while len(self.events) > 0:
			# Retrieve next event and set simulation tick
			sim_time, event = heapq.heappop(self.events)
			self.t = sim_time

			# Execute event
			event.execute(self)









def init_cars():
	"""
	Parses graph files and returns list of Car objects.
	It also caches the result on disk in a pickle archive
	"""

	city_name, scenario = "Luxembourg", "time27100Tper1000.txt"   #DECOMMENT TO USE LUXEMBURG
	#city_name, scenario = "Cologne", "time23000Tper1000.txt"     #DECOMMENT TO USE COLOGNE
	#return init_cars_newyork()									  #DECOMMENT TO USE NEWYORK
	
	fpath = os.path.join("cached", city_name+"_"+scenario+'.bin')
	cached = _load_cached(fpath)
	if cached:	return cached

	print('Computing car graph...')
	positions = []
	p = open("grafi/"+city_name+"/pos/pos_"+scenario, "r")
	for i in p:
		d = i[:-1].split(' ')  #discard trailing \n
		if d[0] == d[2] and d[2] == d[4]:  #append None if it is a malformed row
			positions.append(None)
		else:
			positions.append((float(d[2]), float(d[3])))

	a = open("grafi/"+city_name+"/adj/adj_"+scenario, "r")
	
	cars, i = [], 0
	for line in a:
		if positions[i] != None:
			adi_split = line.split(' ')
			neighbors = [j for j in range(len(adi_split)) if adi_split[j]=='1' and positions[j]!=None]
			cars.append( car.Car(i, positions[i], neighbors) )
		i+=1

	cars = get_largest_conn_component(cars)
	pickle.dump(cars, open(fpath, 'wb'))
	return cars

def init_cars_newyork():
	"""
	New York graph has a different file format, thus needed a different function
	to parse it and load vehicle data
	"""
	fname = 'Newyork5003.mat'
	fpath = os.path.join("cached", fname+'.bin')
	cached = _load_cached(fpath)
	if cached:	return cached

	print('Computing car graph...')
	contents = sio.loadmat(os.path.join('grafi/NewYork/', fname))
	adia, coord = contents['Adia'], contents['coord']
	coord = [(x,y) for x,y in zip(coord[0], coord[1])]
	cars = []
	for i,c,a in zip(range(len(coord)),coord,adia):
		neighbors = [j for j in range(len(a)) if a[j]==1]
		cars.append( car.Car(i, c, neighbors) )

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
	# multiprocessing.Pool only uses functions in the global scope, no lambdas allowed
	return None





def performSimulation(i, verbose=True):
	"""
	Performs a single simulation, with id 'i'
	"""
	# Load vehicle data
	cars = init_cars()

	# Init simulator with the vehicle connectivity graph
	s = Simulator(cars)

	# Get one random car and start the dissemination from it
	if s.no_graphics:
		random.sample(cars, 1)[0].on_receive(Msg.dummy())
	else:
		bubbles = displayCars(s.car_dict)
		firstinfected = s.getCar(firstInfection())
		firstinfected.infect(Msg.dummy())

	# Run simulation
	s.runSimulation()

	# If verbose print the result of this simulation
	if verbose:
		tmp = str([c.state for c in cars])
		print("Simulation", i, "ended")
		print("Vulnerable: ", tmp.count("State.VULNERABLE"))
		print("Infected: ", tmp.count("State.INFECTED"))
		print("Recovered: ", tmp.count("State.RECOVERED"))
		print()

	return s




def performSimulations(n):
	"""
	Performs 'n' different simulations in parallel using multiprocessing.Pool.
	If n==1 the simulation is run without process Pool
	"""

	print('[+] Caching cars data')
	cars_dummy = init_cars()  #trick to cache the car graph on disk before starting the simulation
	print('[+] Done!')

	if n > 1 and N_CPUS > 1:
		with Pool(N_CPUS) as pool:
			print('[+] Starting', n, 'simulations with', N_CPUS, 'parallel jobs')
			sims = pool.map(performSimulation, range(n))
	else:
		sims = [ performSimulation(i) for i in range(n)]
	


	#  ~  All metrics print below  ~

	print()
	print("Average metrics with rmin =",Simulator.RMIN)
	print("#sent messages: ", sum([s.sent_messages for s in sims])/n)
	print("#received messages: ", sum([s.rcv_messages for s in sims])/n)
	print("time of last car infection: ", sum([s.t_last_infected for s in sims])*Simulator.TIME_RESOLUTION/n)
	infected = 0
	for s in sims:
		infected += str([c.state for c in s.cars]).count("State.RECOVERED")
	print("Cars infected ratio: {:.2f}%".format(100*(infected) / (len(sims)*len(sims[0].cars))))
	print("Network traffic (bytes): ", sum([s.network_traffic for s in sims])/n)
	
	# Standard deviation
	#std_dev = 0
	#for s in sims:
	#	std_dev += (str([c.state for c in s.cars]).count("State.RECOVERED")) ** 2
	#std_dev = (std_dev / len(sims))  -  ((infected/len(sims))**2)
	#std_dev = math.sqrt(std_dev)
	#print("Cars infected std dev: {:.2f}".format(std_dev))

	# Distribution of vehicle infection over time
	#t_infected_sum = numpy.zeros(10000)
	#for s in sims:
	#	for t, n in s.t_infected.items():
	#		t_infected_sum[t] += n
	#t_infected_normalized = t_infected_sum / (len(sims)*len(sims[0].cars))
	#pickle.dump(t_infected_normalized, open(f'grafici/runs/t_infected_normalized_TMAX-{Simulator.TMAX*1000}.pickle', 'wb'))



if __name__ == "__main__":
	sys.path.append("./src/")
	if "--with-graphics" in sys.argv:
		performSimulations(1)
	else:
		print('Test mode, to use the visual output run with \'--with-graphics\', need first to install vpython')
		performSimulations(N_SIMULATIONS)
