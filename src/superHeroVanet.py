#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from simulator					import	Simulator, init_cars
from connected_DSC_lib.parser	import	Parser
from connected_DSC_lib.cscalgo	import	CscAlgo
from connected_DSC_lib.gcreator import	Gcreator

cars = init_cars()

sim = Simulator(cars)

parser	=	Parser(sim.car_dict)

parser.CarToInputCSC()

#Input initialization
V	=	parser.V
G	=	parser.G
###################



#V=[1,2,3,4]
#G=[[1,2],[2,1,3],[3,2],[4]]

"""
V=[0,1,2,3,4,5,6,7]
G = [
		[1,2,7],
		[2,1,3,4,5,6],
		[3,2,6],
		[4,2,7],
		[5,2],
		[6,2,3],
		[7,4,1]
	]
"""

################### EXAMPLES

"""
GRAFO A MAGLIA
V=[1,2,3,4,5,6,7]
G = [
		[1,2,7],
		[2,1,3],
		[3,2,4],
		[4,3,5],
		[5,4,6],
		[6,5,7],
		[7,6,1]


]
"""

"""
GRAFO A PERCORSO
V=[1,2,3,4,5,6,7]
G = [
		[1,2],
		[2,1,3],
		[3,2,4],
		[4,3,5],
		[5,4.6],
		[6,5,7],
		[7,6]

]
"""

"""
GRAFO AD ALBERO
V=[1,2,3,4,5,6,7]
G = [
		[1,2,3],
		[2,4,5],
		[3,6,7],
		[4,2],
		[5,2],
		[6,3],
		[7,3]

]

V	=	[1,2,3,4,5,6,7,8,9,10]
G	=	[
			[1,2,3],
			[2,1],
			[3,1,4,7,10],
			[4,3,5],
			[5,4,8,6],
			[6,5,7],
			[7,6,3,9],
			[8,5],
			[9,7],
			[10,3]
		]
"""
#initializate  CSC ALGO
start_time = time.time()
print('Start Algo for: %s nodes' % len(G))

cscAlgo	=	CscAlgo(V,G)

connected_set_cover	=	cscAlgo.doConnectedSetCover()
vertices_csc		=	list(map(lambda x: x[0], connected_set_cover))
len_vertices_csc	=	len(vertices_csc)

print(vertices_csc)

print('End Algo TO CSC use only: %s nodes ' % len_vertices_csc)

print("--- %s seconds ---" % (time.time() - start_time))

