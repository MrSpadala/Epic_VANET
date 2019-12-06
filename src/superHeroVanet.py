#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from simulator			import	Simulator, init_cars
from lib_prog.parser	import	Parser
from lib_prog.cscalgo	import	CscAlgo

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
S=[[1,2],[1],[2],[2,3],[4]]
G=[[1,2],[2,1,3],[3,2],[4]]


#initializate  CSC ALGO
cscAlgo	=	CscAlgo(V,S,G)

# Chose S_0 € S_corsivo s.t. |S_0| is the maximum, and let R={S_0} and U = S_0x



