#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from simulator					import	Simulator, init_cars
from sim_config					import 	config
from connected_DSC_lib.parser	import	Parser
from connected_DSC_lib.cscalgo	import	CscAlgo
from connected_DSC_lib.gcreator import	Gcreator
from connected_DSC_lib.random_graph_gen	import	RandomGraphGen

def execute_alg():

	cars = init_cars()

	sim = Simulator(cars)

	parser	=	Parser(sim.car_dict)

	parser.CarToInputCSC()

	#Input initialization
	V	=	parser.V
	G	=	parser.G
	###################

	n=100
	m=int(n*0.22)	
	grap = RandomGraphGen(100,m)


	V	=	grap.V
	G	=	grap.G
	
	start_time = time.time()
	print('Start Algo for: %s nodes' % len(G))

	cscAlgo	=	CscAlgo(V,G)

	connected_set_cover	=	cscAlgo.doConnectedSetCover()
	vertices_csc		=	list(map(lambda x: x[0], connected_set_cover))
	len_vertices_csc	=	len(vertices_csc)

	print(vertices_csc)

	print('End Algo TO CSC use only: %s nodes ' % len_vertices_csc)

	print("--- %s seconds ---" % (time.time() - start_time))



if __name__ == "__main__":
	city_scenario = {
		"Luxembourg": [
			"time27100Tper1000.txt",
			"time27100Tper50.txt"
		],
		"Cologne": [
			"time23000Tper1000.txt",
			"time23000Tper50.txt"
		],
		"NewYork": [
			"Newyork7005.mat",
			"Newyork3005.mat"
		]
	}

	for city, scenarios in city_scenario.items():
		for i, scenario in enumerate(scenarios):  #two scenarios per city, they must be in order high density then low density
			config.city_name = city
			config.scenario = scenario
			
			print(f"Executing algorithm on {city} {scenario}")
			execute_alg()