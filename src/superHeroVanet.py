#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from simulator					import	Simulator, init_cars
from connected_DSC_lib.parser	import	Parser
from connected_DSC_lib.cscalgo	import	CscAlgo

cars = init_cars()

sim = Simulator(cars)

parser	=	Parser(sim.car_dict)

parser.CarToInputCSC()

#Input initialization
V	=	parser.V
S	=	parser.S
G	=	parser.G
###################


V=[1,2,3,4]
#S=[[1,2],[1],[2],[2,3],[4]]
G=[[1,2],[2,1,3],[3,2],[4]]

"""
G = [
		[0,1,3],
		[1,0,2,7],
		[2,1,3,4,5,6],
		[3,0,2,6],
		[4,2,7],
		[5,2],
		[6,2,3],
		[7,4,1]
	]
"""


#initializate  CSC ALGO
cscAlgo	=	CscAlgo(V,S,G)

# Chose S_0 € S_corsivo s.t. |S_0| is the maximum, and let R={S_0} and U = S_0x



