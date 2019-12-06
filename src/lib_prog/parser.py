#!/usr/bin/env python3
# -*- coding: utf-8 -*-



class Parser:
	def __init__(self, cars):
		self.cars	=	cars
		self.V		=	[]
		self.S		=	[]
		self.G		=	[]


	def CarToInputCSC(self):
		for plate, car in self.cars.items():
			tmpG = [plate] + car.neighbors
			
			self.V.append(plate)
			self.S.append(car.neighbors)
			self.G.append(tmpG)
			
		return True